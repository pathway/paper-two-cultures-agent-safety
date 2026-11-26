# 06 — Citation census: safe RL vs LLM-agent safety (2026-11-20)

Source: `../census/census_report.md`, `../census/metrics.json`. OpenAlex, 2012–2026, keyword-seeded corpora.

| Measure | Safe RL (A, 883 works) | LLM-agent safety (B, 729 works) |
|---|---|---|
| References landing in own corpus | 2,622 (8.1%) | 1,052 (7.4%) |
| References landing in other corpus | 41 (0.13%) | 33 (0.23%) |
| Papers citing the other corpus | 28/883 (3.2%) | 26/729 (3.6%) |
| Authors in both | 44 of 5,092 (Jaccard 0.009) | |
| Venues in both | 25 (Jaccard 0.074) | |
| Louvain vs A/B labels | purity 0.923; NMI 0.42; cross-label edges 74/3,737 (2.0%) | |
| Largest communities | 346 A / 2 B; 0 A / 249 B | |
| B citing canonical safe-RL works | 15/729 (2.1%); 12 cite only Amodei 2016 | |
| A citing canonical LLM-agent works | 24/883; all via "reward hacking" matches | |
| Narrow-query rerun | 0 cross-citations either way; purity 1.000 | |

## Findings
- The split is visible in the citation graph independent of the keyword labels. Null result rejected.
- Nearly all contact runs through one term, "reward hacking": 40/41 A→B and 15/33 B→A citations. Only 6 B papers cite classical safe RL (CPO, Lyapunov, CBF).
- "Concrete Problems" (Amodei 2016) is the lone shared ancestor.
- B→A rate rises 0.0% (2023) → 0.3% (2026).

## Limitations
- Keyword seeding; 200 results per query; OpenAlex's incomplete arXiv reference lists.
- B skews to 2026 (509/729), 378 uncited; "cited ≥ 1" variant gives the same conclusion.
- Safety Gym absent from OpenAlex; canonical check has 5 anchors per side.
- Spend ~$0.03 (OpenAlex metered search); warm-cache rerun is free.

## Use in paper
- Replaces Breiman's 98/2 guess (§1). The "reward hacking" bridge is a result in itself: the single point of contact is the concept that assumes a reward.
