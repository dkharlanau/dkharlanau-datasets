# SAP Sales Process Atlas

A memory-first dataset for SAP sales process variants, deep process traces, reusable sales mechanisms, and high-coverage process normalization.

The author code is intentionally separate from SAP scope-item identifiers:

- `SD.<MNEMONIC>` = process or process family
- `SD.<FAMILY>.<VARIANT>` = meaningful child variant
- `SD.CLM.<VARIANT>` = customer claim / commercial correction family
- `SD.BILL.<VARIANT>` = billing lifecycle / correction family
- `SD+<MNEMONIC>` = overlay or cross-cutting capability
- `MEC.SD.<MNEMONIC>` = reusable decision/control mechanism
- `ORC.SD.<MNEMONIC>` = upstream order origin or orchestrator
- `INT.SD.<MNEMONIC>` = cross-application execution/control handoff
- `EVT.SD.<MNEMONIC>` = asynchronous business-event contract
- `EXT-*` = controlled extension surface

The distinction matters. `SD.SFS + ORC.SD.COMMERCE` and `SD.SFS + ORC.SD.API` are normally the same business process with different order origins. Creating two fake process codes would encode system topology into business semantics and make the graph worse just to make the list longer.

Each detailed process record contains the business intent, flow, control plane, data hinges, downstream impact, constraints, lead-level questions, extension points, and source references.

The process codebook is the entry point. Detailed process records are grouped under `data/` so the dataset can grow without turning one JSON file into a small geological formation.

## High-coverage layer

`sap_sales_process_coverage_v0_2.json` expanded the first map into claims, returns, commercial variants, billing lifecycle and industry execution.

`sap_sales_process_coverage_v0_3.json` adds the cross-application edge. The current normalized map contains **50 process cards/overlays across 11 groups**, plus 15 reusable mechanisms, 9 order-origin patterns and 9 execution-handoff patterns.

The important hierarchy is intentional:

- `SD.RET` = customer returns family
- `SD.RET.LEAN` / `ARM` / `KIT` / `REPAIR` = meaningful reverse-logistics variants
- `SD.CLM.*` = commercial claims without assuming physical return
- `SD.BILL.*` = billing lifecycle/correction variants
- `SD.TPO.*`, `SD.MTO.VC`, `SD.SA.CON`, `SD.JIT` = supply/configuration/industry variants
- `SD.MTO.ATO` = customer-specific assembly directly coupled to sales-order processing
- `SD.ETO` = Engineer-to-Order with WBS/project stock and engineering as part of fulfillment
- `SD.PROJ.PBS` = project-based service sales where customer-project execution supplies the billing evidence
- `SD.SUB.RECUR` = recurring physical delivery where a subscription-style contract generates execution sales orders

SAP scope-item IDs remain aliases/evidence. The ontology primary key stays ours so a release packaging change does not redesign the dataset.

## Cross-application Sales Order layer

`sap_sales_order_integration_map_v0_1.json` answers a different architecture question from the process codebook:

`origin / orchestrator → sales-order business object → next execution owner`

It contains three graph namespaces:

- `ORC.SD.*`: generic API, A2A bulk, external buyer/B2B, SAP Commerce, SAP CPQ, SAP Sales Cloud v2, Solution Order, subscription delivery plan, customer project
- `INT.SD.*`: Production, Project/EPPM, Procurement, EWM, TM, GTS, Credit, Finance, Service
- `EVT.SD.ORDER`: asynchronous Sales Order business events for side-by-side consumers

The core rule is: **origin is not process, integration is not ownership, and a connected application is not automatically a new business branch.**

The Lead-level questions in this layer are therefore different:

1. Is this genuinely a new business process, or only a new order origin?
2. Which system owns price, ATP, credit and configuration when the customer promise is made?
3. Which application owns the next irreversible decision?
4. Which correlation key proves the end-to-end chain across systems?
5. Which calls must be synchronous, and which should be event/message driven?

`data/11_cross_application_execution.json` stores the four business variants that genuinely change the execution model. Order origins and handoffs stay in the integration map instead of being duplicated as process cards.

## Deep control layer

`sap_sales_control_plane_v0_1.json` adds the forward-sales assessment trace:

`document type → item category → schedule line / requirements → supply → stock → goods movement → billing & pricing → integration → failure → test`

The first deep vertical covers `SD.SFS`, `SD.TPO`, `SD.PTO`, `SD.CON`, `SD.ICO`, `SD.AIC`, and `SD.MTO`. Standard SAP keys are stored only where a reviewed public SAP source makes the key explicit; otherwise the dataset stores the behavior instead of pretending a release-specific code is universal.

### Returns and Claims specialized control plane

`sap_sales_return_claims_control_plane_v0_1.json` uses a different grammar because reverse logistics is not simply forward Sales in reverse:

`customer need → reference/reason → release/approval → physical receipt → ownership/stock → inspection/split → logistical follow-up → refund control → valuation/accounting → follow-on documents → integration → failure/test`

Its central memory rule is: **goods received is not the same as goods owned, and goods owned is not the same as customer refunded.**

The file contains ownership states, ARM logistical follow-up activities, refund controls, inspection splits, supplier-return and Service-repair handoffs, failure proofs, and assessment-style tests.

`sap_sales_return_claims_architecture_notes_v0_1.json` stores the choices that are easy to lose in a flow diagram: semantic separation of return reason / inspection / disposition / refund, valuation policy, approval workflow versus billing-block governance, EWM inspection ownership, API-version choice, configurable-material restrictions, and deployment-specific edges.

## Reusable mechanism layer

`sap_sales_mechanism_codebook_v0_1.json` separates reusable system mechanisms from process variants. A process answers **which business branch is running**; a mechanism answers **which decision engine produced this field or behavior**.

The first mechanism library contains 15 stable graph codes across four lanes:

- commercial: item category, partner, pricing, copy control
- fulfillment: schedule line, plant, shipping point, route, scheduling, ATP/aATP, batch determination
- financial: credit management, billing
- communication: text determination, output management

Detailed mechanism records live under `mechanisms/`. They are structured around `question → inputs → output → blast radius → downstream dependencies → failure proof → test`, so they can be reused for graph traversal, study prompts, impact analysis, troubleshooting cases, and assessment simulations.

Primary SAP documentation is used for reference and verification only. Explanations, diagnostic traces, tests, graph decomposition, and memory models are independently authored. Dataset license: CC BY-NC 4.0.
