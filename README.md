# SAP, Enterprise Operations & Agentic AI Datasets — Dzmitryi Kharlanau

[![DOI](https://zenodo.org/badge/1172361882.svg)](https://doi.org/10.5281/zenodo.18862097)
[![Dataset integrity](https://github.com/dkharlanau/dkharlanau-datasets/actions/workflows/dataset-integrity.yml/badge.svg)](https://github.com/dkharlanau/dkharlanau-datasets/actions/workflows/dataset-integrity.yml)

Canonical machine-readable dataset repository curated by **Dzmitryi Kharlanau** for research and reusable work around SAP transformation, enterprise operations, data governance, AI, automation, and agentic systems.

## About

Dzmitryi Kharlanau is an SAP consultant and system analyst working across SAP transformation, SD/MM, MDG, integrations, AMS, data governance, enterprise operations, and practical agentic AI.

This repository publishes reusable dataset bytes created or curated by Dzmitryi Kharlanau for research, learning, and non-commercial reuse with attribution.

- Main website: https://dkharlanau.github.io/
- LinkedIn: https://www.linkedin.com/in/dkharlanau
- Dataset landing page: https://dkharlanau.github.io/datasets/
- Agent-Ready Web Profile: https://github.com/dkharlanau/agent-ready-web-profile

This repository contains machine-readable datasets only. It does not contain the personal website, CV pages, private client data, credentials, or internal enterprise exports.

## Quick start

Clone the repository and validate the complete public collection with Python 3.10+:

```bash
git clone https://github.com/dkharlanau/dkharlanau-datasets.git
cd dkharlanau-datasets
python3 scripts/dataset_registry.py validate
```

Discover records through the manifest instead of assuming a directory layout:

```python
import json
from pathlib import Path

root = Path("datasets")
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

for entry in manifest["entries"]:
    record = json.loads((root / entry["path"]).read_text(encoding="utf-8"))
    print(entry["dataset"], entry["id"], record.get("title"))
```

The repository uses only JSON and a standard-library validator; no package installation
is required for this workflow.

Browse the six collections or search across record identity, title, summary, tags and entity type:

```bash
python3 scripts/query_datasets.py collections
python3 scripts/query_datasets.py search "authority"
python3 scripts/query_datasets.py search "control" --dataset sap-sales-processes --json
```

## Contents

- `datasets/agentic-bytes/` — compact records about agentic systems and patterns
- `datasets/ams/` — SAP AMS / enterprise support material
- `datasets/DAMA/` — data-management knowledge records
- `datasets/LLM-prompts/` — reusable prompt-oriented records
- `datasets/sap-sales-processes/` — SAP Sales Process Atlas codebook and detailed process records
- `datasets/TRIZ-bytes/` — structured TRIZ knowledge records
- `datasets/manifest.json` — dataset discovery manifest
- `datasets/catalog.json` — generated collection-level catalog and coverage summary
- `datasets/schema.json` — shared structural schema

See [`docs/data-contract.md`](docs/data-contract.md) for record identity, supporting-file,
compatibility, and deterministic manifest rules.

See [`docs/discovery-and-reuse.md`](docs/discovery-and-reuse.md) for local search, safe reuse,
and the evidence boundary with Signal to Insight and SAP Agentic Operations.

## Intended use

The repository is designed for transparent reuse in:

- research and comparative analysis
- retrieval and RAG experiments
- structured knowledge systems
- AI-agent evaluation and grounding experiments
- SAP / enterprise process education and diagnostics
- reproducible examples that benefit from stable, citable data

Dataset availability does not make every record authoritative for a production SAP landscape. Validate technical and process decisions against the relevant system, documentation, and organizational context.

## Quality and change workflow

All committed JSON files must parse successfully. Records with `meta.schema` set to
`dkharlanau.dataset.byte` must satisfy the common provenance and attribution contract and
must be present in the generated manifest.

```bash
python3 scripts/dataset_registry.py build     # refresh the manifest after record changes
python3 scripts/dataset_registry.py validate  # validate data and manifest freshness
```

Dataset-specific payloads remain intentionally heterogeneous. Consumers should rely on
the shared metadata for discovery and inspect the domain payload before production use.

## License

The datasets in this repository are licensed under CC BY-NC 4.0:

- Non-commercial use only
- Attribution is mandatory
- Attribution must include a clickable source link to the canonical dataset URL or repository page

See `LICENSE-DATA`.

## Citation

Concept DOI: `10.5281/zenodo.18862098`

Version DOI for `v1.0.0`: `10.5281/zenodo.18862097`

Preferred citation:

Dzmitryi Kharlanau. "Dataset Bytes by Dzmitryi Kharlanau". CC BY-NC 4.0. DOI: 10.5281/zenodo.18862098.

If you cite a specific release, use the version DOI:

Dzmitryi Kharlanau. "Dataset Bytes by Dzmitryi Kharlanau", `v1.0.0`. CC BY-NC 4.0. DOI: 10.5281/zenodo.18862097.

See `CITATION.cff` and `docs/citation.md` for the repository citation guidance.

## Related projects

- [Signal to Insight](https://github.com/dkharlanau/signal-to-insight) can turn selected, independently reviewed source material into a published evidence-backed explainer; dataset records are not auto-published as insights.
- [SAP Agentic Operations](https://github.com/dkharlanau/sap-agentic-operations) uses operational Evidence Packs and may review external research context, but these public datasets never stand in for observations from a production incident.
- [Agent-Ready Web Profile](https://github.com/dkharlanau/agent-ready-web-profile) exposes machine-readable discovery patterns for public knowledge and dataset surfaces.

The canonical public dataset landing page remains https://dkharlanau.github.io/datasets/.

## About the author

Created and maintained by **Dzmitryi Kharlanau**, an SAP consultant and system analyst working across enterprise architecture, data, integration, operations, and practical AI.

- [Website and knowledge base](https://dkharlanau.github.io/)
- [LinkedIn](https://www.linkedin.com/in/dkharlanau/)
