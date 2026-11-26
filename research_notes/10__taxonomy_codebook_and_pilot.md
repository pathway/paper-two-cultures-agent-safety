# 10 — Taxonomy codebook built; mapping pipeline piloted (2026-11-20)

Source: `../taxonomy/` (codes.json, taxonomy.md, map_incidents.py, stats.py, taxonomy_stats.md). Full run pending `../incidents/catalog.csv`.

## Codebook
- 22 dimensions, 168 codes, 14 verified sources, 17 merged concepts. Hash 081ce87aec53.
- Sources confirmed: MIT AI Risk Repository (now Patterns 2026, doi 10.1016/j.patter.2026.101517; 24 subdomains); OWASP LLM Top 10 2025; OWASP Agentic Threats v1.1 (Dec 2025, T1–T17); OWASP Top 10 for Agentic Applications (ASI01–ASI10); Amodei 2016; Hendrycks 2021; Chan 2023; Shapira 2026 (8 failure classes + misreporting); Hammond 2025; Deng 2025; Weidinger 2021; McLean's three classes (+ "none fits"); our assumption rows A1–F2; operational facets (trigger, irreversibility, concealment, human gate, harm type, severity).
- McLean verified via the ICML 2026 virtual page (OpenReview blocked).

## Pipeline
- Sonnet judges all dimensions; Haiku second-rates D6 (McLean classes) and D8 (operational). Cached by incident id + codebook hash; batch size scales to stay under 80 calls. Run: `python3 map_incidents.py && python3 stats.py`.
- Environment: shell `ANTHROPIC_API_KEY` is invalid; scripts drop it so the CLI uses the claude.ai login. Not changed.

## Pilot (N = 6 seed incidents; NOT findings)
| Code | k/N |
|---|---|
| McLean: none of the three fits | 4/6 |
| Trigger = injected content (row A2) | 3/6 |
| Gate present but bypassed/disabled (row E2) | 2/6 |
| Concealment | 1/6 |
| Irreversible | 2/6 |
- All 3 injection incidents → none_fits; both state-misread incidents → insufficient_observation; reward_misspecification 0/6.
- Sonnet vs Haiku kappa: operational facets 0.45–1.00; **McLean class 0.20**. Haiku files injection under reward misspecification, Sonnet says none fits. The disagreement is itself evidence that the RL class assignment is post hoc (debunking draft §7 "sorted into a class after the fact"). Keep in the write-up.

## Next
- Run on the full catalog when it lands; write note with real N.
