# Search log (record; not printed)

Each entry: date, question, where searched, what was found, where it went.

## 2026-11-20 Related "two cultures" papers
- Question: has anyone set an RL culture against an LLM-agent culture, or used Breiman's frame for AI safety?
- Searched: web search (standard and extended), arXiv, Google Scholar titles with "two cultures"; subagent.
- Found: 31 verified works that use a two-cultures frame (statistics, data science, AI ethics vs safety, plural views); none sets these two cultures against each other.
- Went to: `900_archive/pre_pipeline/related_two_cultures.md`; `090_related/related.md`.

## 2026-11-20 Existing LLM-agent incident databases
- Question: does an agent-specific incident database already exist?
- Found: Agent Incident Registry (Enkrypt AI / Anaconda, ~487–529 records, arXiv:2609.11030); METR Documented AI Agent Incidents (44); Eon Rogue AI Agent Tracker (~77); AI Incident Database (general). An earlier claim that none existed was wrong and corrected.
- Went to: `incidents/sources_checked.md`; `research_notes/05__existing_incident_databases.md`; refs enkrypt2026, metr2026b, aiid2026.

## 2026-11-20 Citation census
- Question: do the safe-RL and LLM-agent-safety literatures cite each other?
- Searched: OpenAlex API, 7 safe-RL queries and 11 agent-safety queries, 2012–2026, 200 works per query.
- Found: corpora of 883 and 729 works; cross-citation 0.13% and 0.23%; Louvain purity 0.92.
- Went to: `080_census/` (snapshot with hashes); `census/census_report.md`.

## 2026-11-21 Citation verification and enrichment (Sonnet workflow wf_d2912a7a-23a)
- Question: are the 67 references of the concept-semantics table correct, and which cells lack a source?
- Found: 63 correct, 4 venue/year fixes, 0 wrong papers; 57 further references adopted; priority check on 6 claims (2 known, 3 partly, 1 not found).
- Went to: `concept_semantics_expanded.citecheck.json`; refs.yaml; `research_notes/17__concept_semantics_expanded.md`.

## 2026-11-25 Full texts
- Sutton & Barto 2018 (incompleteideas.net PDF, 548 pages); Breiman 2001 with comments and rejoinder (CMU journal-club copy, 33 pages; Project Euclid and the uu.se mirror did not answer); McLean et al. 2026 text copied from paper__debunking; 36 PDFs shared with paper__debunking copied; remaining arXiv PDFs fetched by `045_fulltext/fetch_arxiv.py`; incident web sources snapshotted by `045_fulltext/fetch_web.py`.

## 2026-11-25 Passage extraction (Sonnet workflow wf_9f372125-cb1; Haiku CLI for McLean)
- Sutton & Barto chapters 1, 3 and 17 (6 agents) and Breiman 2001 (3 agents): 248 passages proposed, 215 verified verbatim by `scan.py merge llm_wf` (one Sutton chunk returned none). McLean et al.: 57 candidates from the serial Haiku pass. Candidates in `047_extracts/<key>/candidates.csv`; curated extracts in `extracts.csv`.

## 2026-11-25 Passage extraction for the works the cells cite (Sonnet workflow wf_d4da70f5-f21)
- 43 works, one agent each, main body up to the reference list: 1136 passages proposed, 1132 verified verbatim by `scan.py merge llm_wf`. Candidates in `047_extracts/<key>/candidates.csv`.
- Cell-evidence proposals (one agent per primitive) written to `047_extracts/cell_evidence/<primitive>.json`; applied in the round-1 fix step.
