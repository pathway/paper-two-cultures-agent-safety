# The Two Cultures of Agents

**What reward, policy, action, observation and transition mean for LLM chatbots and tool agents.**

When an RL researcher and an LLM-agent builder say *agent*, they name different objects. This paper lays the two meanings side by side, one RL primitive at a time (reward, policy, action, observation, state, transition, episode, value), in nine settings: an RL agent in training and in deployment; chat training with an outcome reward model, with a verifier and with a process reward model; agent training; and deployment of a chatbot, of a tool agent with a human between steps and of an autonomous tool agent. It describes the gap and proposes no bridge. Breiman's two cultures [1] name the split.

**Paper:** [`twopager.pdf`](twopager.pdf) (identical to [`paper.pdf`](paper.pdf)). The path `twopager.pdf` is kept from the first release, so earlier links open the current version.

**Status:** Draft, built 2026-11-25 after four review rounds. Most text was written by Claude (Anthropic) under Robin Chauhan's direction and has not been human-reviewed. The property codes were set by LLM raters (two independent Claude Sonnet instances and an adjudicator); no human has checked them. The scope changed on 2026-11-25 from "Agent Safety: The Two Cultures" to the two cultures of agents; the repository name is kept so links do not break.

## How the paper is built

The paper is a build output. Each fact is stored once in a numbered stage folder; the draft (`200_draft/draft.md`) only imports facts and tables; `300_render/build.py` renders the PDF and stops on any failed check (quotes verbatim in the stored source, counts computed not typed, stale claims, unknown references, comparative claims checked against coded properties). `000_README.md` lists the stages.

| Stage | Holds |
|---|---|
| `005_decisions/` | Every scope and inclusion decision, with who decided |
| `040_biblio/`, `047_extracts/`, `050_biblio_notes/` | References, verbatim extracts with locators, per-source notes |
| `060_settings/`, `062_primitives/`, `063_contrasts/`, `064_properties/`, `065_primitive_cells/`, `066_property_codes/` | The settings, the primitives, matched pairs of settings, 23 coded properties, the primitive x setting cells and the property codes |
| `080_census/`, `085_breiman/` | OpenAlex citation census snapshots; Breiman's lines |
| `090_related/`, `095_claims/`, `200_draft/` | Related work, fixed wording with stamps, the draft |
| `100_analysis/` | Pure, tested code that computes every printed number (`facts.json`) |
| `096_review/` | Review rounds: frozen key claims, settled findings, change logs, briefs |
| `300_render/` | Build, checks, the comparative-claim linter, LaTeX template; `out/` holds the built paper |
| `research_notes/` | Working notes, including how two error classes were found and removed (notes 20, 21) |

Not included: `045_fulltext/` (copyrighted source texts; the build's quote and hash checks need it, so `build.py` does not run from this repository alone), round snapshots, and the review agents' raw transcripts. The census code reads the OpenAlex contact address from `OPENALEX_MAILTO`.

## Earlier files (first release, 2026-11-22)

These are the hand-written files of the first release, under the earlier safety scope. They are kept unchanged.

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
| [`twopager.pdf`](twopager.pdf) | The current paper (same file as `paper.pdf`); this path is kept so existing links still work |

## Related repositories

- [paper-rl-limits-llm-agent-safety](https://github.com/pathway/paper-rl-limits-llm-agent-safety)
- [llm-agent-incident-catalog](https://github.com/pathway/llm-agent-incident-catalog)

Part of a set of AI-safety research artefacts by [Robin Ranjit Singh Chauhan](mailto:robin@pathwayi.com), Pathway Intelligence Inc. The website at pathway.github.io/research/ is built from these repositories.

## References

[1] L. Breiman (2001). Statistical Modeling: The Two Cultures. Statistical Science 16(3), 199-231. https://doi.org/10.1214/ss/1009213726
