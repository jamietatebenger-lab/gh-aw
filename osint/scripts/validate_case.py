#!/usr/bin/env python3
"""
validate_case.py

Validate forensic OSINT case and evidence JSON files against the
JSON Schemas stored in ../schema/.

Designed for lawful public-source investigation records.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError:
    print(
        "ERROR: jsonschema is not installed.\n"
        "Install it with:\n"
        "  python -m pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(2)


SCRIPT_DIR = Path(__file__).resolve().parent
OSINT_DIR = SCRIPT_DIR.parent
SCHEMA_DIR = OSINT_DIR / "schema"

CASE_SCHEMA = SCHEMA_DIR / "case.schema.json"
EVIDENCE_SCHEMA = SCHEMA_DIR / "evidence.schema.json"


class ValidationFailure(Exception):
    """Raised when a file cannot be loaded or validated."""


def load_json(path: Path) -> Any:
    """Load JSON from disk with useful error messages."""

    if not path.exists():
        raise ValidationFailure(f"File does not exist: {path}")

    if not path.is_file():
        raise ValidationFailure(f"Not a regular file: {path}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    except json.JSONDecodeError as exc:
        raise ValidationFailure(
            f"Invalid JSON in {path}\n"
            f"Line: {exc.lineno}\n"
            f"Column: {exc.colno}\n"
            f"Reason: {exc.msg}"
        ) from exc

    except OSError as exc:
        raise ValidationFailure(
            f"Unable to read {path}: {exc}"
        ) from exc


def load_validator(schema_path: Path) -> Draft202012Validator:
    """Load and verify a Draft 2020-12 JSON Schema."""

    schema = load_json(schema_path)

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValidationFailure(
            f"Invalid JSON Schema: {schema_path}\n{exc.message}"
        ) from exc

    return Draft202012Validator(schema)


def format_path(parts) -> str:
    """Convert a jsonschema error path into readable notation."""

    result = "$"

    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"

    return result


def validate_document(
    document_path: Path,
    schema_path: Path,
) -> bool:
    """Validate one JSON document."""

    document = load_json(document_path)
    validator = load_validator(schema_path)

    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )

    if not errors:
        print(f"[VALID] {document_path}")
        print(f"        schema: {schema_path.name}")
        return True

    print(f"[INVALID] {document_path}")
    print(f"          schema: {schema_path.name}")
    print(f"          errors: {len(errors)}")

    for number, error in enumerate(errors, start=1):
        location = format_path(error.absolute_path)

        print()
        print(f"  {number}. Location: {location}")
        print(f"     Error: {error.message}")

    return False


def determine_schema(document_type: str) -> Path:
    """Return the schema associated with a document type."""

    if document_type == "case":
        return CASE_SCHEMA

    if document_type == "evidence":
        return EVIDENCE_SCHEMA

    raise ValidationFailure(
        f"Unsupported document type: {document_type}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate forensic OSINT case/evidence JSON "
            "against repository schemas."
        )
    )

    parser.add_argument(
        "document",
        type=Path,
        help="JSON document to validate",
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=("case", "evidence"),
        dest="document_type",
        help="Type of document being validated",
    )

    parser.add_argument(
        "--schema",
        type=Path,
        help="Optional custom schema path",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        schema_path = (
            args.schema
            if args.schema
            else determine_schema(args.document_type)
        )

        valid = validate_document(
            args.document.resolve(),
            schema_path.resolve(),
        )

        return 0 if valid else 1

    except ValidationFailure as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    except KeyboardInterrupt:
        print("\n[INTERRUPTED]", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
