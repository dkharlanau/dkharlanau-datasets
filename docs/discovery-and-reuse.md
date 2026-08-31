# Dataset discovery and safe reuse

The repository contains several domain collections rather than one uniform table. Start with the generated collection catalog, then use the record manifest for stable identity and paths.

## Discover collections

```bash
python3 scripts/query_datasets.py collections
```

Machine-readable catalog:

- [`datasets/catalog.json`](../datasets/catalog.json)

The catalog provides curated collection descriptions, topics, record counts, supporting-file counts, observed tags and entity-type coverage. It is generated and checked together with the manifest.

## Search records

```bash
python3 scripts/query_datasets.py search "authority"
python3 scripts/query_datasets.py search "control" --dataset sap-sales-processes
python3 scripts/query_datasets.py search "governance" --json
```

Search is deterministic and local. It checks record identity, title, summary, tags and entity type. All query terms must match; results are ranked by exact identity and title relevance before stable collection/id ordering.

## Read one record

Use the `(dataset, id)` identity from search results:

```bash
python3 scripts/query_datasets.py show agentic-bytes agentic_dev_001
```

Do not construct file paths from record ids. Resolve the path through `datasets/manifest.json`, because directory layout may evolve while public identities remain stable.

## Use with Signal to Insight

A dataset record may be considered as source material, but repository presence does not make it an independently verified claim.

1. Inspect the record's provenance and attribution.
2. Follow its canonical or upstream source when available.
3. Queue the source through the normal Signal to Insight intake and review lifecycle.
4. Keep copied source material out of the public repository.
5. Export only an explicitly published insight through the research-evidence handoff.

There is intentionally no bulk “publish these records as insights” command.

## Use with SAP Agentic Operations

These collections are useful for learning, control-design discussion and synthetic examples. They are not production incident evidence.

Do not put a dataset record into an SAO Evidence Pack as proof that a system event occurred. Operational evidence must identify the actual business object, system, observation time and provenance for the bounded case.

The portable Signal to Insight handoff provides a safer route for reviewed public research context:

```bash
sao research validate research-evidence.json
```

Even a valid handoff remains `external_research_context` and cannot authorize execution.

## Citation and license

Dataset records are available under CC BY-NC 4.0 with attribution. Use the concept DOI for the evolving collection or the version DOI for an exact release. See [citation guidance](citation.md) for the preferred format.
