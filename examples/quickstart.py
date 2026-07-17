"""Quickstart: a chat completion and a model listing, with the sync client.

Reads the API key from the ``GALENE_AI_API_KEY`` environment variable (and,
optionally, a non-default host from ``GALENE_AI_BASE_URL``). Run with::

    GALENE_AI_API_KEY=sk-... uv run python examples/quickstart.py
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
        reply = client.chat.create(
            model="Galene/LLM",
            messages=[{"role": "user", "content": "Say hello in one short sentence."}],
        )
        print(reply.choices[0].message.content)

        models = client.models.list()
        model_ids = [m.get("id") for m in models.get("data", [])]
        print(f"available models: {model_ids}")


if __name__ == "__main__":
    main()
