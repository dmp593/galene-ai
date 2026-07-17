from galene_ai._core.retry import RetryPolicy


def test_retries_on_429_and_503_within_budget():
    p = RetryPolicy(max_retries=2)
    assert p.should_retry(0, status=429, method="GET", is_timeout=False)
    assert p.should_retry(1, status=503, method="POST", is_timeout=False)
    assert not p.should_retry(2, status=503, method="GET", is_timeout=False)  # budget spent


def test_does_not_retry_400():
    p = RetryPolicy(max_retries=3)
    assert not p.should_retry(0, status=400, method="GET", is_timeout=False)


def test_does_not_retry_nonidempotent_timeout():
    # POST timeout must NOT retry — a duplicate generation would hang server-side.
    p = RetryPolicy(max_retries=3)
    assert not p.should_retry(0, status=None, method="POST", is_timeout=True)
    assert p.should_retry(0, status=None, method="GET", is_timeout=True)


def test_backoff_honors_retry_after():
    p = RetryPolicy(max_retries=3)
    assert p.backoff_seconds(0, retry_after=5.0) == 5.0
    assert 0 < p.backoff_seconds(0, retry_after=None) <= 2.0
