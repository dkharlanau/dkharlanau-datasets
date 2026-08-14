# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants and cross-process overlays.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process variant
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `EXT-*` = controlled extension surface

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The codebook is the entry point. Detailed process records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

## Deep control layer

`sap_sales_control_plane_v0_1.json` adds a second, assessment-oriented layer. It traces selected sales processes through:

`document type → item category → schedule line / requirements → supply → stock → goods movement → billing & pricing → integration → failure → test`

The first deep vertical covers `SD.SFS`, `SD.TPO`, `SD.PTO`, `SD.CON`, `SD.ICO`, `SD.AIC`, and `SD.MTO`. Standard SAP keys are stored only where a reviewed public SAP source makes the key explicit; otherwise the dataset stores the behavior instead of pretending a release-specific code is universal.

Primary SAP documentation is used for reference and verification only. Explanations, diagnostic traces, tests, and memory models are independently authored. Dataset license: CC BY-NC 4.0.
