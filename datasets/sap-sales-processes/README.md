# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants, deep process traces, and reusable sales mechanisms.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process variant
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `MEC.SD.<MNEMONIC>` = reusable decision/control mechanism
- `EXT-*` = controlled extension surface

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The process codebook is the entry point. Detailed process records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

## Deep control layer

`sap_sales_control_plane_v0_1.json` adds the assessment-oriented process trace:

`document type → item category → schedule line / requirements → supply → stock → goods movement → billing & pricing → integration → failure → test`

The first deep vertical covers `SD.SFS`, `SD.TPO`, `SD.PTO`, `SD.CON`, `SD.ICO`, `SD.AIC`, and `SD.MTO`. Standard SAP keys are stored only where a reviewed public SAP source makes the key explicit; otherwise the dataset stores the behavior instead of pretending a release-specific code is universal.

## Reusable mechanism layer

`sap_sales_mechanism_codebook_v0_1.json` separates reusable system mechanisms from process variants. A process answers **which business branch is running**; a mechanism answers **which decision engine produced this field or behavior**.

The first mechanism library contains 15 stable graph codes across four lanes:

- commercial: item category, partner, pricing, copy control
- fulfillment: schedule line, plant, shipping point, route, scheduling, ATP/aATP, batch determination
- financial: credit management, billing
- communication: text determination, output management

Detailed mechanism records live under `mechanisms/`. They are structured around `question → inputs → output → blast radius → downstream dependencies → failure proof → test`, so they can be reused for graph traversal, study prompts, impact analysis, troubleshooting cases, and assessment simulations.

Primary SAP documentation is used for reference and verification only. Explanations, diagnostic traces, tests, graph decomposition, and memory models are independently authored. Dataset license: CC BY-NC 4.0.
