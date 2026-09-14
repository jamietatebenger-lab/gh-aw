#!/usr/bin/env python3
"""
Public-source entity correlation engine.

Compares two structured records and produces:
- weighted similarity score
- matching attributes
- conflicting attributes
- missing attributes
- confidence classification

A high score is an investigative lead, not proof of identity.
"""

import argparse
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


WEIGHTS = {
    "name": 30,
    "date_of_birth": 25,
    "locations": 10,
    "organisations": 12,
    "associates": 8,
    "usernames": 8,
    "domains": 7,
}


def normalise(value):
    """Normalise text for comparison."""
    if value is None:
        return ""

    value = str(value)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        c for c in value
        if not unicodedata.combining(c)
    )
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)

    return " ".join(value.split())


def as_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def similarity(a, b):
    a = normalise(a)
    b = normalise(b)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    return SequenceMatcher(None, a, b).ratio()


def best_list_similarity(left, right):
    left = as_list(left)
    right = as_list(right)

    if not left or not right:
        return None

    best = 0.0
    pair = None

    for a in left:
        for b in right:
            score = similarity(a, b)

            if score > best:
                best = score
                pair = (a, b)

    return best, pair


def compare_name(a, b):
    names_a = [a.get("name")] + as_list(a.get("aliases"))
    names_b = [b.get("name")] + as_list(b.get("aliases"))

    names_a = [x for x in names_a if x]
    names_b = [x for x in names_b if x]

    return best_list_similarity(names_a, names_b)


def compare_exact(a, b, field):
    left = a.get(field)
    right = b.get(field)

    if not left or not right:
        return None

    return (
        1.0 if normalise(left) == normalise(right) else 0.0,
        (left, right),
    )


def compare_lists(a, b, field):
    return best_list_similarity(
        a.get(field),
        b.get(field)
    )


def confidence_label(score, contradictions):
    if contradictions and score >= 85:
        return "HIGH_SCORE_WITH_CONTRADICTIONS"

    if score >= 85:
        return "STRONG_CANDIDATE"

    if score >= 70:
        return "PROBABLE_CANDIDATE"

    if score >= 50:
        return "POSSIBLE_CANDIDATE"

    if score >= 30:
        return "WEAK_CANDIDATE"

    return "INSUFFICIENT_MATCH"


def correlate(a, b):
    comparisons = {
        "name": compare_name(a, b),
        "date_of_birth": compare_exact(
            a, b, "date_of_birth"
        ),
        "locations": compare_lists(
            a, b, "locations"
        ),
        "organisations": compare_lists(
            a, b, "organisations"
        ),
        "associates": compare_lists(
            a, b, "associates"
        ),
        "usernames": compare_lists(
            a, b, "usernames"
        ),
        "domains": compare_lists(
            a, b, "domains"
        ),
    }

    weighted_score = 0.0
    available_weight = 0

    matches = []
    contradictions = []
    missing = []
    detail = {}

    for field, result in comparisons.items():
        weight = WEIGHTS[field]

        if result is None:
            missing.append(field)
            continue

        score, pair = result

        available_weight += weight
        weighted_score += score * weight

        detail[field] = {
            "similarity": round(score, 4),
            "weight": weight,
            "values": pair,
        }

        if score >= 0.85:
            matches.append({
                "field": field,
                "similarity": round(score, 4),
                "values": pair,
            })

        # Treat conflicting DOB as a major warning.
        if field == "date_of_birth" and score == 0:
            contradictions.append({
                "field": field,
                "severity": "HIGH",
                "values": pair,
            })

        # Strongly different names are worth reviewing.
        elif field == "name" and score < 0.45:
            contradictions.append({
                "field": field,
                "severity": "MEDIUM",
                "values": pair,
            })

    if available_weight:
        final_score = (
            weighted_score / available_weight
        ) * 100
    else:
        final_score = 0.0

    final_score = round(final_score, 2)

    return {
        "entity_a": a.get("id", "A"),
        "entity_b": b.get("id", "B"),
        "score": final_score,
        "confidence": confidence_label(
            final_score,
            contradictions
        ),
        "matching_attributes": matches,
        "contradictions": contradictions,
        "missing_attributes": missing,
        "comparison_detail": detail,
        "warning": (
            "Correlation scores support investigative "
            "triage only and do not establish identity."
        ),
    }


def load_json(filename):
    path = Path(filename)

    if not path.is_file():
        raise SystemExit(
            f"Input file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Cross-correlate two public-source "
            "entity records."
        )
    )

    parser.add_argument(
        "entity_a",
        help="First JSON entity record"
    )

    parser.add_argument(
        "entity_b",
        help="Second JSON entity record"
    )

    parser.add_argument(
        "--output",
        help="Optional output JSON filename"
    )

    args = parser.parse_args()

    entity_a = load_json(args.entity_a)
    entity_b = load_json(args.entity_b)

    result = correlate(entity_a, entity_b)

    output = json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )

    if args.output:
        Path(args.output).write_text(
            output + "\n",
            encoding="utf-8"
        )
    else:
        print(output)


if __name__ == "__main__":
    main()
