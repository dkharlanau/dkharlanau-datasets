#!/usr/bin/env python3
"""Search and inspect the public dataset catalog without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "datasets" / "manifest.json"
CATALOG = ROOT / "datasets" / "catalog.json"


class QueryError(ValueError):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QueryError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise QueryError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def terms(value: str) -> list[str]:
    return [term for term in re.split(r"[^a-z0-9]+", value.casefold()) if term]


def searchable_text(entry: dict[str, Any]) -> str:
    values: list[str] = []
    for field in ("dataset", "id", "title", "summary", "entity_type"):
        value = entry.get(field)
        if isinstance(value, str):
            values.append(value)
    values.extend(tag for tag in entry.get("tags", []) if isinstance(tag, str))
    return " ".join(values).casefold()


def search_records(
    entries: list[dict[str, Any]],
    query: str,
    dataset: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    query_terms = terms(query)
    if not query_terms:
        raise QueryError("search query must contain at least one letter or digit")
    matches: list[tuple[int, dict[str, Any]]] = []
    for entry in entries:
        if dataset and entry.get("dataset") != dataset:
            continue
        haystack = searchable_text(entry)
        if not all(term in haystack for term in query_terms):
            continue
        title = str(entry.get("title") or "").casefold()
        identifier = str(entry.get("id") or "").casefold()
        score = sum(haystack.count(term) for term in query_terms)
        if query.casefold() == identifier:
            score += 20
        if query.casefold() in title:
            score += 10
        if title.startswith(query.casefold()):
            score += 5
        matches.append((score, entry))
    matches.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("dataset", "")).casefold(),
            str(item[1].get("id", "")).casefold(),
        )
    )
    return [entry for _, entry in matches[: max(1, limit)]]


def record_by_identity(entries: list[dict[str, Any]], dataset: str, record_id: str) -> dict[str, Any]:
    matches = [
        entry
        for entry in entries
        if entry.get("dataset") == dataset and entry.get("id") == record_id
    ]
    if len(matches) != 1:
        raise QueryError(
            f"expected one manifest entry for ({dataset!r}, {record_id!r}); found {len(matches)}"
        )
    path = ROOT / "datasets" / str(matches[0]["path"])
    return load_object(path)


def print_collections(catalog: dict[str, Any], as_json: bool) -> None:
    collections = catalog.get("collections")
    if not isinstance(collections, list):
        raise QueryError("catalog collections must be a list")
    if as_json:
        print(json.dumps(collections, ensure_ascii=False, indent=2))
        return
    for collection in collections:
        print(
            f"{collection['id']}: {collection['record_count']} record(s), "
            f"{collection['supporting_file_count']} supporting file(s)"
        )
        print(f"  {collection['description']}")


def print_search(results: list[dict[str, Any]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    if not results:
        print("No matching dataset records.")
        return
    for entry in results:
        print(f"{entry['dataset']}/{entry['id']} — {entry['title']}")
        print(f"  {entry['summary']}")
        print(f"  datasets/{entry['path']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    collections = sub.add_parser("collections", help="List curated dataset collections")
    collections.add_argument("--json", action="store_true")
    search = sub.add_parser("search", help="Search manifest title, summary, tags and identity")
    search.add_argument("query")
    search.add_argument("--dataset")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--json", action="store_true")
    show = sub.add_parser("show", help="Print one complete record by collection and id")
    show.add_argument("dataset")
    show.add_argument("record_id")
    args = parser.parse_args()
    try:
        manifest = load_object(MANIFEST)
        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise QueryError("manifest entries must be a list")
        if args.command == "collections":
            print_collections(load_object(CATALOG), args.json)
        elif args.command == "search":
            print_search(
                search_records(entries, args.query, dataset=args.dataset, limit=args.limit),
                args.json,
            )
        else:
            print(
                json.dumps(
                    record_by_identity(entries, args.dataset, args.record_id),
                    ensure_ascii=False,
                    indent=2,
                )
            )
    except QueryError as exc:
        print(f"Dataset query failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
