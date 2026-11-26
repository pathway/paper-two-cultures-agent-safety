# 16. Concept-semantics table: RL vs LLM base model vs LLM agent

Date: 2026-11-21. Source: `../concept_semantics.md` (single source; do not duplicate the table here).

## What it is

- 28 core concepts (rows) in four groups: agent/environment, objective/value, learning/knowledge, safety/oversight.
- Three columns: classical RL, LLM base model, LLM agent with tools. Fourth column links each row to `assumptions_table.md` rows A1–F2.
- Differs from `assumptions_table.md`: that file lists assumptions and who holds them; this file fixes what each shared word denotes.

## Headline findings

- Six RL concepts keep their meaning for agents (action, transition, horizon, failure, adversary, validation) but vanish in the base-model column.
- Six RL concepts never recover at run time: reward, return, value, exploration, learning, episode reset.
- Four agent concepts have no RL counterpart: observation-as-command, three-party specification, self-model of oversight, scaffold-held memory.
- The agent inherits state, action, learning, competence, norms and self-model from the base model, not from RL. The scaffold adds side effects only.

## Use in paper

- Candidate for §3 of the full draft, before the assumptions table: define terms, then state assumptions.
- Supports the §5 claim that "Bellman's curse" and "reward hacking" transfer only under reinterpretation.
- Two-pager: no room; cite the file.

## Open

- Row count may be trimmed to ~15 for a paper table.
- Cells are my readings, not surveyed; no model-judged numbers in this file.
