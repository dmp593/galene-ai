"""RAG walkthrough: upload a file, create a vector store, attach the file, search it.

Run with::

    GALENE_AI_API_KEY=sk-... uv run python examples/vector_store_rag.py
"""

from __future__ import annotations

import os
import sys

from galene_ai import Galene
from galene_ai.models._generated import (
    VectorStoreCreate,
    VectorStoreFileAdd,
    VectorStoreSearchRequest,
)


def main() -> None:
    api_key = os.environ.get("GALENE_AI_API_KEY")
    if not api_key:
        print("Set GALENE_AI_API_KEY to run this example.", file=sys.stderr)
        raise SystemExit(1)

    with Galene(api_key=api_key) as client:
        uploaded = client.files.upload(
            b"Galene.AI ships an OpenAI-compatible vector store API.\n",
            purpose="user_data",
            filename="notes.txt",
        )
        print(f"uploaded file: {uploaded.id}")

        vector_store = client.vector_stores.create(VectorStoreCreate(name="rag-example"))
        print(f"created vector store: {vector_store.id}")

        client.vector_stores.add_file(vector_store.id, VectorStoreFileAdd(file_id=uploaded.id))
        print(f"attached file {uploaded.id} to vector store {vector_store.id}")

        results = client.vector_stores.search(
            vector_store.id, VectorStoreSearchRequest(query="vector store API")
        )
        for item in results.data:
            print(f"{item.filename!r} score={item.score:.4f}")


if __name__ == "__main__":
    main()
