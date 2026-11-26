# 03 — Prior "two cultures" papers (2026-11-20)

Full table: `../related_two_cultures.md` (31 verified citations).

## Headline
- No paper sets an RL/objective-modeling culture against an LLM-agent/behavior-modeling culture. Coverage of forum posts and workshop papers is partial.

## Closest partial pre-emptions
- Turner 2022, "Reward is not the optimization target": RL policies need not maximize reward (attacks the RL culture's core assumption from inside RL).
- Çağatan & Zhao 2026 (arXiv:2606.15385): RL safety gridworlds ported to LLM agents; specification gaming appears without task training; RL fine-tuning worsens it.
- Dantas et al. 2026 (arXiv:2608.14590): LLM-agent safety survey; specification is the bottleneck; zero mentions of safe RL or CMDPs.
- Vernade, Szepesvári, Krstic et al. 2026 (arXiv:2608.02433): RL and control have "distinct methodologies, goals, and cultures"; no Breiman, no Snow.

## Name collision
- "Two cultures of AI safety" already means ethics vs safety (Bristow et al. 2023; Roytburg & Miller 2025; Gyevnár & Kasirzadeh 2026). None cites Breiman or Snow. The intro must say our split is a different one.

## Best supporting citations
- Donoho 2017: Common Task Framework as the predictive culture's "secret sauce" → evals-as-specification (rows F1, F2).
- D'Amour 2021; Rudin 2025: Rashomon sets → an eval suite does not pin down the agent.
- Carrington & Stocks 1994, formal methods vs testing → SE ancestor of shields vs evals.
- Observational Studies 7(1), 2021: Breiman retrospective with ~30 comments, incl. Ogburn & Shpitser "Causal Modelling: The Two Cultures" and Pearl's reply (neither Breiman culture gives intervention guarantees).

## Caveats
- Ogburn & Shpitser not read (DOI only). Bertsekas never uses "two cultures"; do not cite him for it.
