"""Async usage: AsyncGalene chat completion + file upload, driven by asyncio.run.

``AsyncGalene`` mirrors ``Galene`` method-for-method. Run with::

    GALENE_AI_API_KEY=sk-... uv run python examples/async_usage.py
"""

from __future__ import annotations

import asyncio
import os
import sys

from galene_ai import AsyncGalene


async def main() -> None:
    api_key = os.environ.get("GALENE_AI_API_KEY")
    if not api_key:
        print("Set GALENE_AI_API_KEY to run this example.", file=sys.stderr)
        raise SystemExit(1)

    async with AsyncGalene(api_key=api_key) as client:
        reply = await client.chat.create(
            model="Galene/LLM",
            messages=[{"role": "user", "content": "Hi there"}],
        )
        print(reply.choices[0].message.content)

        uploaded = await client.files.upload(
            b"Hello from the galene-ai async example.\n",
            purpose="user_data",
            filename="hello.txt",
        )
        print(f"uploaded file: {uploaded.id}")


if __name__ == "__main__":
    asyncio.run(main())
