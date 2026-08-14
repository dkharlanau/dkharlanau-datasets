# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants, deep process traces, reusable sales mechanisms, and high-coverage process normalization.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process family
- `SD.<FAMILY>.<VARIANT>` = meaningful child variant
- `SD.CLM.<VARIANT>` = customer claim / commercial correction family
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `MEC.SD.<MNEMONIC>` = reusable decision/control mechanism
- `EXT-*` = controlled extension surface

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The process codebook is the entry point. Detailed process records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

## High-coverage layer

`sap_sales_process_coverage_v0_2.json` expands the process taxonomy from a core learning map into a practical coverage map. It adds 22 normalized records for claims, returns, billing, settlement, payment, third-party subvariants, configurable products and JIT supply.

The important hierarchy is intentional:

- `SD.RET` = customer returns family
- `SD.RET.LEAN` = simple receipt-to-stock + credit
- `SD.RET.ARM` = Advanced Returns Management with inspection, disposition and refund logic
- `SD.RET.KIT` = returns for sales kits
- `SD.RET.REPAIR` = return-to-Service repair handoff
- `SD.CLM.CMR` / `DMR` / `ICR` / `FOS` = credit, debit, invoice correction, and free replacement claims
- `SD.TPO.SN` / `NSN` / `VC` = third-party execution variants
- `SD.MTO.VC`, `SD.SA.CON`, `SD.JIT` = configuration/industry execution variants

The coverage file also normalizes SAP scope-item IDs onto stable author codes. For example, BDN maps to `SD.PTO`, while Advanced ATP (1JW) maps to `MEC.SD.ATP` because ATP is a reusable mechanism rather than a new business branch.

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
