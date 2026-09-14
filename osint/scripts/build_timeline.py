#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from pathlib import Path

CONFIDENCE = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "UNVERIFIED": 0,
}

DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y",
)


def parse_date(value):
    if not value:
        return None, "UNKNOWN"

    value = str(value).strip()

    try:
        dt = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        return dt.replace(tzinfo=None), dt.date().isoformat()
    except ValueError:
        pass

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            return dt, value if fmt == "%Y" else dt.date().isoformat()
        except ValueError:
            continue

    return None, value


def normalize(record, number):
    raw_date = (
        record.get("event_date")
        or record.get("date")
        or record.get("publication_date")
        or record.get("collected_utc")
    )

    sort_date, display_date = parse_date(raw_date)

    confidence = str(
        record.get("confidence", "UNVERIFIED")
    ).upper()

    if confidence not in CONFIDENCE:
        confidence = "UNVERIFIED"

    return {
        "timeline_id": record.get(
            "timeline_id", f"T-{number:04d}"
        ),
        "evidence_id": record.get("evidence_id", ""),
        "date": display_date,
        "_sort_date": sort_date,
        "subject": record.get("subject", ""),
        "event": record.get(
            "event", record.get("claim", "")
        ),
        "location": record.get("location", ""),
        "organisation": record.get(
            "organisation",
            record.get("company", "")
        ),
        "associates": record.get("associates", []),
        "source": record.get(
            "source", record.get("url", "")
        ),
        "source_type": record.get("source_type", ""),
        "confidence": confidence,
        "notes": record.get("notes", ""),
    }


def find_conflicts(records):
    evidence_dates = {}

    for record in records:
        evidence_id = record["evidence_id"]

        if evidence_id:
            evidence_dates.setdefault(
                evidence_id, set()
            ).add(record["date"])

    return {
        evidence_id
        for evidence_id, dates in evidence_dates.items()
        if len({d for d in dates if d != "UNKNOWN"}) > 1
    }


def build_timeline(records):
    timeline = [
        normalize(record, number)
        for number, record in enumerate(records, 1)
    ]

    conflicts = find_conflicts(timeline)

    for record in timeline:
        record["date_conflict"] = (
            record["evidence_id"] in conflicts
        )

    timeline.sort(
        key=lambda r: (
            r["_sort_date"] is None,
            r["_sort_date"] or datetime.max,
            -CONFIDENCE[r["confidence"]],
        )
    )

    for record in timeline:
        record.pop("_sort_date", None)

    return timeline


def make_markdown(timeline):
    lines = [
        "# Forensic OSINT Timeline",
        "",
        "| Date | Subject | Event | Location | Confidence | Evidence |",
        "|---|---|---|---|---|---|",
    ]

    for r in timeline:
        warning = " ⚠ DATE CONFLICT" if r["date_conflict"] else ""

        event = str(r["event"]).replace("|", "\\|")
        subject = str(r["subject"]).replace("|", "\\|")
        location = str(r["location"]).replace("|", "\\|")

        lines.append(
            f"| {r['date']} | {subject} | "
            f"{event}{warning} | {location} | "
            f"{r['confidence']} | {r['evidence_id']} |"
        )

    return "\n".join(lines)


def load_records(path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

   
