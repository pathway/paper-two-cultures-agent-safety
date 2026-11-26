# The Two Cultures of Agents — source pipeline

The paper is generated. Facts and judgements live in the stage folders; the draft imports them; `300_render/build.py` turns everything into the PDF. Each fact is stored once. Method: `../paper__debunking/000_METHOD.md`.

Scope (decisions D2, D9, D12, D13): the RL-agent culture and the LLM-agent culture mean different objects by *agent*. The paper describes that gap, primitive by primitive, in training and in deployment for both, and proposes no bridge. The stamped scope line is `095_claims/claims.csv` id `scope_purpose`. Safety material (075 incidents, 078 labels, 070 assumptions) stays stored but is not imported by the draft.

## Stages

A stage reads only from stages with lower numbers.

| Stage | Holds | Kind |
|---|---|---|
| `005_decisions/decisions.csv` | Each choice of scope or inclusion: who decided, the author's words, the basis | record |
| `010_target/` | The RL reader's own definitions: Sutton & Barto's agent–environment interface and reward hypothesis (`sutton2018.md`); McLean et al. 2026, the paper that asserts the identity (`mclean2026.md`); verified quotes with locators | facts |
| `020_search/` | Search log: related two-cultures papers, incident databases, citation enrichment runs | record (not printed) |
| `040_biblio/` | `refs.yaml`: one entry per work (`key`, `short`, `year`, `text`). `existence.csv`: output of `verify.py` | facts |
| `045_fulltext/` | `pdf/<key>.pdf`, `<key>.txt` (pages separated by form feeds), `tex/<key>/`, `web/<id>.txt` snapshots of incident sources, `manifest.csv` with hashes. Copyrighted: keep out of public copies | facts |
| `047_extracts/<key>/` | `candidates.csv` (scanner output), `extracts.csv` (curated passages cited by id). `PROTOCOL.md`: the topics, one per RL primitive | facts |
| `050_biblio_notes/<key>.md` | Per source: read scope, findings, verified quotes | facts |
| `060_settings/settings.csv` | The settings (columns): phase, how the decision problem is posed, decision id | judgement |
| `062_primitives/primitives.csv` | The RL primitives (rows): id, name, Sutton & Barto definition with extract ids | judgement |
| `065_primitive_cells/cells.csv` | Primitive × setting: value, reason, `evidence_type`, `evidence` (extract ids), `by` | judgement |
| `070_assumptions/assumptions.csv` | A1–F2: the assumptions each culture makes, owner, the primitive each bears on | judgement |
| `075_incidents/incidents.csv` | The 70-incident catalog: fields, assumption tags, sources with snapshots | judgement |
| `078_incident_labels/` | Model-judged labels per incident (coverage: writable rule, failure class; taxonomy codes), with rater and run id. `by` is LLM until audited | judgement |
| `080_census/` | OpenAlex corpora and `metrics.json` (snapshot, hashed) | facts |
| `085_breiman/cultures.csv` | Breiman's two cultures and the discussants' lines, with extract ids | judgement |
| `090_related/related.md` | Related-work prose | argument |
| `095_claims/claims.csv` | Fixed wording the paper prints, with dependencies and stamps | judgement |
| `100_analysis/` | `analyze.py` (pure, tested) → `facts.json`, `sensitivity.md` | computed |
| `200_draft/draft.md` | Prose and imports only | argument |
| `300_render/` | `build.py`, `render.py`, `checks.py`, `backcheck.py`, template; output in `out/` | presentation |
| `096_review/` | `key.csv` (frozen core claims), `rejected.csv` (settled findings), rounds | record |
| `900_archive/` | `pre_pipeline/`: the hand-written files this pipeline replaces (two-pager v0.1, framing, tables); round snapshots | not used |

The earlier working folders `census/`, `coverage/`, `incidents/`, `taxonomy/`, `research_notes/` remain as the record of how the data were produced; the pipeline stages import from them once and the stage files are then the source of truth.

## Build

```
cd 300_render && python3 build.py
cd 100_analysis && python3 -m pytest -q
cd 300_render && python3 -m pytest -q
cd 047_extracts && python3 -m pytest -q
cd 040_biblio && python3 -m pytest -q
cd 096_review && python3 -m pytest -q
```

## Rules

- Change a fact or judgement in its stage file, never in the draft.
- A quote enters a note or a cell only after it has been checked against the stored full text; the build re-checks every quote.
- A count in the prose is a `{{fact:…}}`, never typed.
- `by` records who made a judgement (`LLM`, author, RL reader). All cells are `LLM` until a reader checks them.
- Model-judged incident labels print with the marker [U] until audited (D5).
