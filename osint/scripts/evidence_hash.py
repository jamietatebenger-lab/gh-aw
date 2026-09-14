#!/usr/bin/env python3

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for block in iter(lambda: file.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Create a forensic evidence record."
    )

    parser.add_argument("file")
    parser.add_argument("--id", dest="evidence_id")
    parser.add_argument("--case", dest="case_id")
    parser.add_argument("--source")

    args = parser.parse_args()
    path = Path(args.file).expanduser().resolve()

    if not path.is_file():
        raise SystemExit("Evidence file not found")

    record = {
        "evidence_id": args.evidence_id,
        "case_id": args.case_id,
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "source": args.source,
        "collected_utc": datetime.now(timezone.utc).isoformat()
    }

    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
