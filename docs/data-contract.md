# Dataset contract

This repository distinguishes between **registered records** and **supporting JSON files**.

## Registered records

A registered record is a top-level JSON object with a `meta` object whose `schema` is
`dkharlanau.dataset.byte`. It must provide:

- a stable `id` or `byte_id`;
- a non-empty title, either on the record or in `meta`;
- a dataset name matching the first directory below `datasets/`;
- source project and source path provenance;
- creator and attribution information;
- string-only tags when tags are present.

Every registered record appears in [`datasets/manifest.json`](../datasets/manifest.json).
The pair `(dataset, id)` is unique across the repository.

Collection-level descriptions and aggregate coverage appear in the generated
[`datasets/catalog.json`](../datasets/catalog.json). Curated titles, descriptions and topics
come from `config/dataset-collections.json`; counts, entity types and observed tags are derived
from the actual records.

## Supporting JSON files

Some datasets split a larger model into smaller group files. These files remain public,
versioned, and JSON-validated, but they do not claim to be independently citable dataset
records and therefore do not appear as separate manifest entries. Their parent dataset
README explains how the components fit together.

## Deterministic registry

The manifest is generated from record metadata. Its timestamp is derived from the most
recent record timestamp rather than the machine clock, so the same repository content
always produces the same manifest.

Build or refresh it:

```bash
python3 scripts/dataset_registry.py build
```

Validate every JSON file, record identity, required metadata, manifest freshness and collection
catalog freshness:

```bash
python3 scripts/dataset_registry.py validate
```

The `Dataset integrity` GitHub Actions workflow runs the validator for every change to
`main` and for pull requests.

## Compatibility

- Existing record identifiers should be treated as stable public identifiers.
- Additive fields are preferred over destructive schema changes.
- A changed interpretation should use versioned metadata or a new record when consumers
  could otherwise confuse old and new semantics.
- The shared schema is intentionally permissive because the domain payloads differ. The
  registry validator enforces the common discovery and attribution contract.
