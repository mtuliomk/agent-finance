#!/usr/bin/env python3
"""Summarize a local position CSV without interpreting prices or refreshing custody."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def summarize(path, missing, group):
    counts = Counter()
    total = selected = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if len(set(fields)) != len(fields):
            raise ValueError("duplicate CSV headers")
        for field in (missing, group):
            if field and field not in fields:
                raise ValueError(f"unknown field: {field}")
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"invalid CSV row at line {reader.line_num}")
            total += 1
            if missing and row[missing].strip() not in ("", "[pending]"):
                continue
            selected += 1
            if group:
                counts[row[group].strip() or "[unknown]"] += 1
    return {
        "file": str(path),
        "scope": "local CSV only; custody date and completeness not inferred",
        "total_rows": total,
        "missing_field": missing,
        "selected_rows": selected,
        "group_by": group,
        "groups": dict(sorted(counts.items())),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--missing", help="Select rows with empty or [pending] field")
    parser.add_argument("--group", help="Count selected rows by this field")
    args = parser.parse_args()
    try:
        result = summarize(args.file, args.missing, args.group)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
