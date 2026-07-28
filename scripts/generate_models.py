# scripts/generate_models.py
"""Regenerate msgspec models from the vendored OpenAPI spec.

Dev-only. Output is committed and never hand-edited.
Run: python scripts/generate_models.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.json"
OUT = ROOT / "src" / "galene_ai" / "models" / "_generated.py"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            str(SPEC),
            "--input-file-type",
            "openapi",
            "--output",
            str(OUT),
            "--output-model-type",
            "msgspec.Struct",
            "--target-python-version",
            "3.12",
            "--use-annotated",
            "--use-standard-collections",
            "--use-union-operator",
            # No generation timestamp in the header — otherwise the committed file
            # never matches a fresh run and the models-fresh CI job always fails.
            "--disable-timestamp",
            "--formatters",
            "ruff-format",
        ],
        check=True,
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
