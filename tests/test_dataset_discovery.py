from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dataset_registry import (  # noqa: E402
    CATALOG_PATH,
    MANIFEST_PATH,
    build_catalog,
    build_manifest,
    collection_config,
    registry_records,
    serialized_manifest,
)
from query_datasets import QueryError, record_by_identity, search_records  # noqa: E402


class DatasetDiscoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records, cls.record_errors = registry_records()
        cls.collections, cls.collection_errors = collection_config()
        cls.manifest = build_manifest(cls.records)
        cls.catalog = build_catalog(cls.records, cls.collections)

    def test_registry_and_collection_config_are_valid(self) -> None:
        self.assertEqual(self.record_errors, [])
        self.assertEqual(self.collection_errors, [])
        self.assertEqual(len(self.collections), 6)

    def test_generated_discovery_files_are_current(self) -> None:
        self.assertEqual(
            MANIFEST_PATH.read_text(encoding="utf-8"),
            serialized_manifest(self.manifest),
        )
        self.assertEqual(
            CATALOG_PATH.read_text(encoding="utf-8"),
            serialized_manifest(self.catalog),
        )

    def test_catalog_counts_reconcile_to_manifest(self) -> None:
        self.assertEqual(self.catalog["record_count"], self.manifest["count"])
        self.assertEqual(
            sum(item["record_count"] for item in self.catalog["collections"]),
            self.manifest["count"],
        )
        self.assertEqual(self.catalog["supporting_file_count"], 15)

    def test_search_is_case_insensitive_and_dataset_scoped(self) -> None:
        entries = [
            {
                "dataset": "alpha",
                "id": "A-1",
                "title": "Identity Resolution",
                "summary": "Resolve a business object across systems.",
                "tags": ["identity"],
                "entity_type": "pattern",
                "path": "alpha/a-1.json",
            },
            {
                "dataset": "beta",
                "id": "B-1",
                "title": "Identity Policy",
                "summary": "A different record.",
                "tags": [],
                "entity_type": "policy",
                "path": "beta/b-1.json",
            },
        ]
        results = search_records(entries, "IDENTITY", dataset="alpha")
        self.assertEqual([item["id"] for item in results], ["A-1"])
        with self.assertRaises(QueryError):
            search_records(entries, "---")

    def test_manifest_identity_resolves_to_full_record(self) -> None:
        first = self.manifest["entries"][0]
        record = record_by_identity(self.manifest["entries"], first["dataset"], first["id"])
        self.assertIn(record.get("id") or record.get("byte_id"), {first["id"]})


if __name__ == "__main__":
    unittest.main()
