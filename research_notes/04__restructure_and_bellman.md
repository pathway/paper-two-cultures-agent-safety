# 04 — Restructure around the table; Bellman decision (2026-11-20)

## Changes
- `framing.md` §3 rebuilt around the six row groups of `assumptions_table.md` (A Objective, B Learning, C Environment/state, D Actions/observations, E Overseer, F Validation). Each body section: RL default, LLM default, RL steelman, consequence, Breiman analogue.
- Breiman lessons attached to groups: no-power-of-goodness-of-fit → A; Rashomon → B; frozen toolkit and Cox → C; Occam → D; new community and information-from-a-black-box → E; predictive accuracy and Efron → F.
- §4 evidence anchored to rows: census → §1 and E; coverage count → A5, D1; Rashomon demo → B2, B3; transfer test P1–P6 → A1, A4, A5, B1, C2, E1.
- Bibliography 26 → 44 entries, no orphans.

## Bellman decision: cut as a section, keep the curse
- Test: two cited results with no classical-RL counterpart plus a tight analogy.
- Found one: Baker et al. 2025, CoT monitoring beats action monitoring; a weaker model can monitor a stronger one. Korbak et al. 2025 is a position paper ("fragile").
- Instructability has a goal-conditioned RL counterpart and is the same channel as prompt injection. AgentSpec is a shield with a DSL front end.
- Analogy is decorative: Breiman's blessing is the predictor using more features; ours would be the overseer reading more output.
- CoT monitoring moves to group E under Breiman §11 ("information from a black box").
