"""Streaming chat completion: print each SSE delta chunk as it arrives.

``chat.create(..., stream=True)`` returns a ``Stream[dict]`` — chunks decode
as plain dicts in the standard OpenAI delta shape (the API spec defines no
fixed chunk schema). Run with::

    GALENE_AI_API_KEY=sk-... uv run python examples/streaming.py
"""

from __future__ import annotations

import os
import sys

from galene_ai import Galene


def main() -> None:
    api_key = os.environ.get("GALENE_AI_API_KEY")
    if not api_key:
        print("Set GALENE_AI_API_KEY to run this example.", file=sys.stderr)
        raise SystemExit(1)

    with Galene(api_key=api_key) as client:
        # stream=True always returns a Stream[dict]; use it as a context manager so
        # the underlying HTTP response is closed once streaming is done.
        with client.chat.create(
            model="Galene/LLM",
            messages=[{"role": "user", "content": "Count from 1 to 5."}],
            stream=True,
        ) as stream:
            for chunk in stream:
                choices = chunk.get("choices") or []
                delta = choices[0].get("delta") if choices else {}
                print((delta or {}).get("content") or "", end="", flush=True)
        print()


if __name__ == "__main__":
    main()
