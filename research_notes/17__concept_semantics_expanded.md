# 17. Expanded concept-semantics table: six decision settings

Date: 2026-11-21 (v4). Source: `../concept_semantics_expanded.md` (single source; 124 refs with URLs, per-cell citations, §7 provenance). Raw citation-check output: `../concept_semantics_expanded.citecheck.json`.

## Columns

- RL: MDP/POMDP.
- CHAT-O: no tools, whole completion = one action, learned reward model. Bandit with proxy reward.
- CHAT-V: no tools, whole trace + answer = one action, programmatic verifier (RLVR, R1-style). Bandit with ground-truth reward; trace unsupervised.
- CHAT-P: no tools, step = action, PRM. Deterministic tree MDP, dense reward.
- AGENT-A: tool assistant, human between turns. Episodic POMDP.
- AGENT-X: autonomous loop, no human between steps, memory, sub-agents. Long-horizon POMDP, no reset.

v1 → v2: added CHAT-V; added rows "the KL term" and "sim-to-real"; added §0 stating the three independent axes (action granularity, reward source, world coupling) the columns move along.

v2 → v3: added rows belief state, reward identifiability, instrumental behaviour, planning/world model, on- vs off-policy, what RL adds to the base model, contract view, autonomy level, defence layer, monitorability. Refs 52–67. Four new §6 bullets (identifiability gradient, instrumental behaviour as theorem vs eval finding, planning survives only in CHAT-P, stacked incomplete contracts).

## Rows

- 46 concepts in five groups: formal objects; objective/reward/value; learning/exploration/search; world/parties; safety/oversight.

## Headline findings

- CHAT-O/V are bandits; the field dropped the critic (RLOO, GRPO). The only classical-RL object that survives there is the KL trust region, which works as a constraint on drift from the prior.
- CHAT-P is the setting where RL theory literally applies (dense reward, Markov, known dynamics, resets, search) and has no side effects. The frontier retreated from it because the PRM got hacked (R1, Zhang 2025).
- CHAT-V's unsupervised trace is a new oversight channel that training pressure destroys (Baker 2025); agents inherit this.
- AGENT-X is furthest from RL on every formal row, yet is where RL vocabulary is used most. Sim-to-real reappears as sandbox-to-deployment.
- McLean's three classes land in different columns: misspecification in CHAT-O/V/P, irreversible action in AGENT-X, insufficient observation in AGENT-A/X. No column has all three.
- Catalog incidents sit in AGENT-A/X; RL-safety constructions sit in RL and CHAT-P. The two cultures look at different columns.

## Use in paper

- Candidate §3 figure: the six-column gradient with McLean's classes placed on it.
- Supports framing.md §5 (analogy breaks) and twopager §6 (words transfer, objects do not).
- The KL-as-CMDP observation is new; check whether anyone has stated it (candidate short section or footnote).

## Open

- Sixth-axis candidates not covered: multi-agent as own column; PRM over tool calls (agent process reward).
- Cells are my readings, not surveyed; no model-judged numbers.
- Not independently verified by a human.

## Citation workflow results (Sonnet, run wf_d2912a7a-23a, 2026-11-21)

Shape: 10 agents, 306 tool calls, 0 errors. 4 verifiers over refs 1–67; 5 enrichers, one per row group; 1 priority check on 6 claims.

Verification of refs 1–67:
- 63 correct as written. 4 fixes applied: Sharma sycophancy is ICLR 2024 not 2023; DeepSeek-R1 has a Nature citation; Zverev is ICLR 2025; SWE-RL is NeurIPS 2025. 4 optional venue additions applied. 0 not found.
- The initial memory-written list had no wrong paper and no wrong URL. Errors were venue/year only.

Enrichment: 67 suggestions, 57 adopted as refs 68–124. Dropped: duplicates, unverified (Silver "Reward is enough"), and marginal fits. Biggest gaps filled: the RL column (was citing Sutton & Barto for everything; now PPO, TRPO, CPO, Bellemare, Pinto, Lowe, Krakovna, Eysenbach, Leike, CIRL, off-switch), the AGENT-A column (τ-bench, ToolEmu, InjecAgent, ArCHer), jailbreak sources, and the instrumental-behaviour row.

Priority check on six §6 claims:

| Claim | Verdict | Key prior statements |
|---|---|---|
| KL penalty = CMDP-style constraint on drift from prior | known | Moskovitz 2024 (RLHF as CMDP, KL coefficient as Lagrange multiplier); Gao 2023 "KL budget"; Ziegler 2019 adaptive KL target; Jaques 2017 KL-control; Korbak 2022 Bayesian reading |
| RLHF is a contextual bandit; critic dropped | known | Ahmadian 2024; ReMax 2024; Xiong 2024; Lambert RLHF book §6.3 |
| CHAT-P closest to RL, abandoned because PRM hacked | partly | retreat known (R1 §G.2, Feng 2025, Gao 2024, Cheng 2025); ranking of settings not found |
| Identifiability degrades across settings | partly | rungs 1–2 explicit (Skalse 2023; DPO Def. 1); rung 3 informal (verifier pitfalls); rung 4 not found |
| Instrumental behaviour: theorem in RL, role-play in agents | partly | components known separately (Turner; Shanahan role-play; Lynch triggers); evidence mixed: He 2025 says RL raises it, Alparslan 2026 says non-monotone |
| McLean's three classes in three different settings | not found | 5 searches; third-party summary words McLean's classes as observation ambiguity / reward misspecification / unsafe exploration (check against the paper) |

Consequences for the paper:
- Drop "the KL term is the one object that survives" as a claim of novelty; keep it as framing with [73, 19, 12].
- The identifiability gradient (rung 4: no reward object at run time) and the McLean-classes-to-settings mapping are the two candidates for original contributions from this table.
- New related work found by the check: Ng et al. 2026 "Agent safety should be a runtime contract" (arXiv 2608.11274) argues the same relocation of safety to run time as the pivot in notes 07–09. Must be cited in framing.md §6 and the two-pager related work. Cagatan & Zhao 2026 (arXiv 2606.15385) port AI Safety Gridworlds to LLM agents; relevant to §5 of framing.
- Check McLean's exact class names against the paper before using them in a table.
