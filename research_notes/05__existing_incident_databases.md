# 05 — Do LLM-agent incident databases already exist? (2026-11-20, corrected after verification)

Source: `../incidents/sources_checked.md` §"Existing incident databases" (each opened and inspected).

## Answer: yes, three are agent-specific
| Database | URL | Size | Notes |
|---|---|---|---|
| **Agent Incident Registry (AIR)**, Enkrypt AI / Anaconda | https://air.enkryptai.com (paper arXiv:2609.11030) | 487–529 source-linked records 2022–2026, ~200 with realized harm | Verbatim-quote rule; taxonomy of causal role / disclosure class / mechanism / outcome. **Closest peer to our catalog; best external cross-check and a candidate larger N for our measurements.** |
| **METR, Documented AI Agent Incidents** | https://metr.org/agent-incidents/ | 44 (18 METR evals, 24 public, 2 anonymous), through 2026-05-19 | Scored on overreach and deception |
| **Eon, Rogue AI Agent Tracker** | https://www.eon.io/rogue-ai-agent-tracker | ~77 (33 accidents, 18 agent-assisted attacks, 5 eval escapes) | Production damage focus |

## Not agent-specific (my earlier provisional list was right on these)
- AI Incident Database: no agent tag, but entity pages ("LLM-integrated code assistants", "Claude Code", "Cursor", "Gemini CLI") act as filters. Most useful general source.
- OECD AIM (~19k entries; autonomy-level filter only), AIAAIC, MIT AI Risk Repository + Incident Tracker, AVID (covers prompt injection; latest 2026-03), OWASP incident round-ups (no agentic tag), Vibe Graveyard (mixed).
- Simon Willison's prompt-injection tag (163 posts) and Embrace The Red (~50 product exploits) are de facto agent-exploit indexes, unstructured.

## Consequence for the paper
- Our catalog is not a first. Cite AIR, METR and Eon; position ours by its fields (trigger, approval-gate status, assumption-table codes) and by the measurements run on it.
- Option: rerun coverage and taxonomy over AIR's ~500 records for a 5× larger N. Not started (cost); needs a decision.
- My 2026-11-20 chat answer ("no agent-specific database exists as far as I know") was wrong on this point.
