# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants and cross-process overlays.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process variant
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `EXT-*` = controlled extension surface

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The codebook is the entry point. Detailed records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

Primary SAP documentation is used for reference and verification only. Explanations and memory models are independently authored. Dataset license: CC BY-NC 4.0.
