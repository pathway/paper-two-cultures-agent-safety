# "Two Cultures" paper

Breiman [1] split statistics into a data-modelling and an algorithmic culture; agent safety has the same split. One culture (safe RL, constrained MDPs, shields) begins "assume the agent maximises a reward R". The other (red teams, evals, AI control, incident reports) treats the agent as a black box and measures what it does. The paper maps the two line by line, counts how often each side's assumptions fail across 70 real incidents, and traces both in the citation graph. A two-page draft (v0.1, 2026-11-20) is written; the full paper is not.

**Status:** Started. Most text was written by Claude (Anthropic) under Robin Chauhan's direction and has not been human-reviewed.

Start with `framing.md`; `twopager.md` is the short version.

## Contents

| File | Title |
|---|---|
| [`assumptions_table.md`](assumptions_table.md) | Unified assumptions table: classical RL vs LLM agents |
| [`census/bridge.csv`](census/bridge.csv) |  |
| [`census/census_report.md`](census/census_report.md) | Do safe RL and LLM-agent safety cite each other? A citation census |
| [`census/census_tables.md`](census/census_tables.md) | Census tables |
| [`census/corpus_A.csv`](census/corpus_A.csv) |  |
| [`census/corpus_B.csv`](census/corpus_B.csv) |  |
| [`concept_semantics.md`](concept_semantics.md) | Semantics of core concepts: RL, LLM base model, LLM agent with tools |
| [`concept_semantics_expanded.md`](concept_semantics_expanded.md) | Semantics of core concepts across six decision settings |
| [`framing.md`](framing.md) | Agent Safety: The Two Cultures — framing notes |
| [`related_two_cultures.md`](related_two_cultures.md) | Related work: "two cultures" framings (for "Agent Safety: The Two Cultures") |
| [`twopager.md`](twopager.md) | Agent Safety: The Two Cultures |
| [`twopager.pdf`](twopager.pdf) |  |


## Related repositories

- [paper-rl-limits-llm-agent-safety](https://github.com/pathway/paper-rl-limits-llm-agent-safety)
- [llm-agent-incident-catalog](https://github.com/pathway/llm-agent-incident-catalog)

Part of a set of AI-safety research artefacts by [Robin Ranjit Singh Chauhan](mailto:robin@pathwayi.com), Pathway Intelligence Inc. The website at pathway.github.io/research/ is built from these repositories.

## References

[1] L. Breiman (2001). Statistical Modeling: The Two Cultures. Statistical Science 16(3), 199-231. https://doi.org/10.1214/ss/1009213726
