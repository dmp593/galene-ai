from __future__ import annotations

import random

_RETRY_STATUSES = frozenset({408, 409, 429, 500, 502, 503, 504})
_IDEMPOTENT = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})
_BASE_DELAY = 0.5
_MAX_DELAY = 8.0


class RetryPolicy:
    def __init__(self, max_retries: int) -> None:
        self.max_retries = max_retries

    def should_retry(
        self, attempt: int, *, status: int | None, method: str, is_timeout: bool
    ) -> bool:
        if attempt >= self.max_retries:
            return False
        if is_timeout:
            # Only retry timeouts on idempotent methods (avoid duplicate generations).
            return method.upper() in _IDEMPOTENT
        if status is None:  # connection error, not a timeout
            return method.upper() in _IDEMPOTENT
        return status in _RETRY_STATUSES

    def backoff_seconds(self, attempt: int, retry_after: float | None) -> float:
        if retry_after is not None and retry_after >= 0:
            return retry_after
        delay: float = min(_BASE_DELAY * (2**attempt), _MAX_DELAY)
        return delay * (0.5 + random.random() * 0.5)  # 50–100% jitter
