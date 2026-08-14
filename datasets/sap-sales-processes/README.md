# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants, deep process traces, reusable sales mechanisms, and high-coverage process normalization.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process family
- `SD.<FAMILY>.<VARIANT>` = meaningful child variant
- `SD.CLM.<VARIANT>` = customer claim / commercial correction family
- `SD.BILL.<VARIANT>` = billing lifecycle / correction family
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `MEC.SD.<MNEMONIC>` = reusable decision/control mechanism
- `EXT-*` = controlled extension surface

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The process codebook is the entry point. Detailed process records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

## High-coverage layer

`sap_sales_process_coverage_v0_2.json` expands the process taxonomy from a core learning map into a practical coverage map. It now normalizes 46 process cards/overlays across 10 groups, with 26 additions over the original core map.

The important hierarchy is intentional:

- `SD.RET` = customer returns family
- `SD.RET.LEAN` = simple receipt-to-stock + credit
- `SD.RET.ARM` = Advanced Returns Management with inspection, disposition and refund logic
- `SD.RET.KIT` = returns for sales kits
- `SD.RET.REPAIR` = return-to-Service repair handoff
- `SD.CLM.CMR` / `DMR` / `ICR` / `INC` / `FOS` = credit, debit, invoice correction, invoice increase, and free replacement claims
- `SD.BILL.COLL` / `PRELIM` / `RETRO` / `CANCEL` = billing consolidation, pre-invoice negotiation, retrospective repricing, and cancellation
- `SD.TPO.SN` / `NSN` / `VC` = third-party execution variants
- `SD.MTO.VC`, `SD.SA.CON`, `SD.JIT` = configuration/industry execution variants

The coverage file also normalizes SAP scope-item IDs onto stable author codes. For example, BDN maps to `SD.PTO`, while Advanced ATP (1JW) maps to `MEC.SD.ATP` because ATP is a reusable mechanism rather than a new business branch. Distinct but not-yet-deepened candidates such as configurable-material returns (7KW) and classic down payment processing (BKJ) stay explicit rather than being incorrectly merged into newer variants.

## Deep control layer

`sap_sales_control_plane_v0_1.json` adds the forward-sales assessment trace:

`document type → item category → schedule line / requirements → supply → stock → goods movement → billing & pricing → integration → failure → test`

The first deep vertical covers `SD.SFS`, `SD.TPO`, `SD.PTO`, `SD.CON`, `SD.ICO`, `SD.AIC`, and `SD.MTO`. Standard SAP keys are stored only where a reviewed public SAP source makes the key explicit; otherwise the dataset stores the behavior instead of pretending a release-specific code is universal.

### Returns and Claims specialized control plane

`sap_sales_return_claims_control_plane_v0_1.json` uses a different grammar because reverse logistics is not simply forward Sales in reverse:

`customer need → reference/reason → release/approval → physical receipt → ownership/stock → inspection/split → logistical follow-up → refund control → valuation/accounting → follow-on documents → integration → failure/test`

Its central memory rule is: **goods received is not the same as goods owned, and goods owned is not the same as customer refunded.**

The file contains:

- ownership states from customer-owned product to non-valuated returns stock, valuated stock and final disposition
- a normalized map of high-value ARM logistical follow-up activities such as `0001`, `0002`, `0005`, `0007`, `0021`, `0023`, and `0026`
- refund controls `R / P / I / N` and their different effects for credit versus replacement
- a deep `SD.RET.ARM` trace with inspection splits, ownership/valuation, supplier return and Service repair handoffs
- process boundaries for `SD.RET.LEAN`, `SD.CLM.CMR`, `SD.CLM.DMR`, `SD.CLM.ICR`, `SD.CLM.INC`, and `SD.CLM.FOS`
- failure proofs and small assessment-style tests rather than only process descriptions

`sap_sales_return_claims_architecture_notes_v0_1.json` sits above the process trace and stores the Lead-level choices that are easy to lose in a flow diagram: semantic separation of return reason / inspection / disposition / refund, valuation policy, approval-workflow versus billing-block governance, EWM inspection ownership, API-version choice, configurable-material restrictions, and deployment-specific edges.

## Reusable mechanism layer

`sap_sales_mechanism_codebook_v0_1.json` separates reusable system mechanisms from process variants. A process answers **which business branch is running**; a mechanism answers **which decision engine produced this field or behavior**.

The first mechanism library contains 15 stable graph codes across four lanes:

- commercial: item category, partner, pricing, copy control
- fulfillment: schedule line, plant, shipping point, route, scheduling, ATP/aATP, batch determination
- financial: credit management, billing
- communication: text determination, output management

Detailed mechanism records live under `mechanisms/`. They are structured around `question → inputs → output → blast radius → downstream dependencies → failure proof → test`, so they can be reused for graph traversal, study prompts, impact analysis, troubleshooting cases, and assessment simulations.

Primary SAP documentation is used for reference and verification only. Explanations, diagnostic traces, tests, graph decomposition, and memory models are independently authored. Dataset license: CC BY-NC 4.0.
