#!/usr/bin/env python3
"""Build and validate the public dataset registry without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DATASETS_ROOT = REPOSITORY_ROOT / "datasets"
MANIFEST_PATH = DATASETS_ROOT / "manifest.json"
REGISTRY_EXCLUSIONS = {"manifest.json", "schema.json"}
REQUIRED_META_FIELDS = (
    "schema",
    "schema_version",
    "dataset",
    "source_project",
    "source_path",
    "creator",
    "attribution",
)


class RegistryError(ValueError):
    """Raised when a dataset or registry contract is invalid."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryError(f"{path.relative_to(REPOSITORY_ROOT)}: invalid JSON: {exc}") from exc


def dataset_paths() -> list[Path]:
    return sorted(
        path
        for path in DATASETS_ROOT.rglob("*.json")
        if path.name not in REGISTRY_EXCLUSIONS
    )


def title_from_identifier(identifier: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[_-]+", " ", identifier)).strip().title()


def validate_record(path: Path, document: Any) -> list[str]:
    errors: list[str] = []
    relative_path = path.relative_to(DATASETS_ROOT).as_posix()

    if not isinstance(document, dict):
        return [f"{relative_path}: top-level JSON value must be an object"]

    meta = document.get("meta")
    if meta is None:
        # Component files are valid public JSON but are registered through their
        # parent dataset rather than as independent dataset bytes.
        return errors
    if not isinstance(meta, dict):
        return [f"{relative_path}: meta must be an object"]

    for field in REQUIRED_META_FIELDS:
        if field not in meta:
            errors.append(f"{relative_path}: meta.{field} is required")

    if meta.get("schema") != "dkharlanau.dataset.byte":
        errors.append(f"{relative_path}: meta.schema must be dkharlanau.dataset.byte")

    expected_dataset = path.relative_to(DATASETS_ROOT).parts[0]
    if meta.get("dataset") != expected_dataset:
        errors.append(
            f"{relative_path}: meta.dataset must match its directory ({expected_dataset})"
        )

    identifier = document.get("id") or document.get("byte_id")
    if not isinstance(identifier, str) or not identifier.strip():
        errors.append(f"{relative_path}: id or byte_id must be a non-empty string")

    title = document.get("title") or meta.get("title")
    if title is not None and (not isinstance(title, str) or not title.strip()):
        errors.append(f"{relative_path}: title must be a non-empty string when present")

    tags = document.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(f"{relative_path}: tags must be an array of strings")

    creator = meta.get("creator")
    if not isinstance(creator, dict):
        errors.append(f"{relative_path}: meta.creator must be an object")
    else:
        for field in ("name", "role"):
            if not isinstance(creator.get(field), str) or not creator[field].strip():
                errors.append(f"{relative_path}: meta.creator.{field} is required")

    attribution = meta.get("attribution")
    if not isinstance(attribution, dict):
        errors.append(f"{relative_path}: meta.attribution must be an object")
    else:
        if attribution.get("attribution_required") is not True:
            errors.append(f"{relative_path}: attribution_required must be true")
        if not isinstance(attribution.get("preferred_citation"), str):
            errors.append(f"{relative_path}: preferred_citation must be a string")

    return errors


def registry_records() -> tuple[list[tuple[Path, dict[str, Any]]], list[str]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []
    identities: dict[tuple[str, str], str] = {}

    for path in dataset_paths():
        try:
            document = load_json(path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue

        errors.extend(validate_record(path, document))
        if not isinstance(document, dict) or not isinstance(document.get("meta"), dict):
            continue

        meta = document["meta"]
        identifier = document.get("id") or document.get("byte_id")
        if not isinstance(identifier, str) or not isinstance(meta.get("dataset"), str):
            continue

        identity = (meta["dataset"], identifier)
        relative_path = path.relative_to(DATASETS_ROOT).as_posix()
        if identity in identities:
            errors.append(
                f"{relative_path}: duplicate dataset identity {identity!r}; "
                f"first defined by {identities[identity]}"
            )
        else:
            identities[identity] = relative_path
        records.append((path, document))

    return records, errors


def normalized_timestamp(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def manifest_timestamp(records: list[tuple[Path, dict[str, Any]]]) -> str:
    timestamps: list[datetime] = []
    for _, document in records:
        meta = document["meta"]
        for field in ("updated_at_utc", "created_at_utc", "generated_at_utc"):
            value = meta.get(field)
            if isinstance(value, str) and (parsed := normalized_timestamp(value)):
                timestamps.append(parsed)
    if not timestamps:
        raise RegistryError("No record timestamp is available for deterministic manifest generation")
    return max(timestamps).isoformat(timespec="seconds")


def build_manifest(records: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for path, document in records:
        meta = document["meta"]
        identifier = document.get("id") or document.get("byte_id")
        title = document.get("title") or meta.get("title") or title_from_identifier(identifier)
        summary = meta.get("summary") or document.get("summary") or title
        entries.append(
            {
                "dataset": meta["dataset"],
                "id": identifier,
                "title": title,
                "path": path.relative_to(DATASETS_ROOT).as_posix(),
                "tags": document.get("tags", []),
                "entity_type": meta.get("entity_type") or "dataset_byte",
                "summary": summary,
            }
        )

    entries.sort(key=lambda entry: (entry["dataset"], entry["id"], entry["path"]))
    return {
        "schema": "dkharlanau.dataset.manifest",
        "schema_version": "1.1",
        "generated_at_utc": manifest_timestamp(records),
        "license": {
            "name": "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
            "spdx": "CC-BY-NC-4.0",
            "url": "https://creativecommons.org/licenses/by-nc/4.0/",
        },
        "attribution": {
            "attribution_required": True,
            "preferred_citation": (
                "Dzmitryi Kharlanau. Dataset bytes (manifest). CC BY-NC 4.0. "
                "https://dkharlanau.github.io/datasets/manifest.json"
            ),
        },
        "creator": {
            "name": "Dzmitryi Kharlanau",
            "role": "SAP Lead",
            "website": "https://dkharlanau.github.io",
            "linkedin": "https://www.linkedin.com/in/dkharlanau",
        },
        "datasets_root": "datasets",
        "count": len(entries),
        "entries": entries,
    }


def serialized_manifest(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def run(command: str) -> int:
    records, errors = registry_records()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Dataset validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    expected = serialized_manifest(build_manifest(records))
    if command == "build":
        MANIFEST_PATH.write_text(expected, encoding="utf-8")
        print(f"Wrote {MANIFEST_PATH.relative_to(REPOSITORY_ROOT)} with {len(records)} records.")
        return 0

    actual = MANIFEST_PATH.read_text(encoding="utf-8") if MANIFEST_PATH.exists() else ""
    if actual != expected:
        print(
            "ERROR: datasets/manifest.json is stale; run "
            "python3 scripts/dataset_registry.py build",
            file=sys.stderr,
        )
        return 1

    component_count = len(dataset_paths()) - len(records)
    print(
        f"Validated {len(records)} registered records and {component_count} supporting JSON files; "
        "manifest is current."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check", "validate"))
    args = parser.parse_args()
    return run(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
