# 20. The phase confound: where the deployed-RL vs deployed-LLM error came from, and how to remove the class

Date: 2026-11-25. Trigger: author, "is there reward when RL agents are deployed?" and "the deployed-RL vs deployed-LLM framing is wrong".

## The error class
A difference caused by the phase axis (training vs deployment) is attributed to the culture axis (RL vs LLM). The paper compares RL in training with LLMs in deployment, and reads the result as a property of LLMs.

## Origin (traced)
1. `900_archive/pre_pipeline/concept_semantics.md` (v1, 2026-11-21): one RL column, filled from the textbook. The textbook describes the training loop, so "RL" silently meant RL training. The LLM columns described deployed systems.
2. `assumptions_table.md` rows B1 "Does the policy learn at deployment: RL yes" and B2 "Does a reward signal arrive at deployment: RL yes, each step". Both are false for a deployed RL policy. They were written from intuition, cited no source, and became stage 070 unchanged.
3. When D-RL was added (decision D3, copying the companion paper's phase split), its cells were filled honestly ("not used; policy fixed", "none used"). The headline facts were not recomputed as contrasts. `llm_deployment_no_reward` counts a property over the LLM deployment settings only, and never asks whether D-RL shares it.
4. Key claim K01 froze the same one-sided statement, so every reviewer scored it "supported": the statement is true; it is only not distinctive.

## Why five review passes missed it
- Scorers and finders test truth of a claim against tables and sources. A one-sided claim is true. No lens tests whether a claimed difference is a difference.
- The key encoded the confound, so review measured against the error.
- Comparisons were computed on free-text label strings (round-1 finding F1.4), so even the cell-comparison facts could not express "same property".

## Same confound still present (2026-11-25 scan)
- Draft: "in the deployment settings there is no reward to hack and no designed exploration"; "nothing resets" and "no learned value function" in LLM deployment; conclusion "lose their reward and value in every LLM deployment setting"; "where its central object is absent (every LLM deployment setting)"; "the deployed agent is still frozen, unrewarded and unreset". Each holds for D-RL too, or partly.
- Stage 070 rows A1, B1, B2, C2, E2, E3 contrast RL training with LLM deployment. 070 is not printed (D12) but is a stored judgement.
- Cells: value D-RL "none used" vs D-* "none"; reward D-RL "not used" vs "none". The labels hide which property differs.

## What does differ (candidate, for the gate)
- Reward: whether a reward function is defined for the deployed task (D-RL yes, the designer's R; D-LLM no, the objective is a prompt). Not whether reward is used for learning (neither).
- Episode: whether the deployed environment was designed with resets (some D-RL yes; D-LLM no).
- Observation: whether observations can carry instructions (D-RL no; D-LLM yes).
- Policy: whether the deployer can change behaviour without retraining (D-RL no; D-LLM yes, by prompt and scaffold).

## Permanent removal (pipeline changes, proposed as D15)
1. **Coded properties, not labels.** Each primitive gets 2–4 named yes/no/partly properties (e.g. reward: defined_for_task, used_for_learning, arrives_per_step, scalar). Stage `064_properties/properties.csv` defines them with their source; `065` cells carry a code per property. Labels stay for display only.
2. **Matched contrasts only.** `060_settings` gets `matched_rl` (T-* → T-RL, D-* → D-RL). `analyze.py` computes every difference fact as setting vs its matched RL setting on codes. A property shared with the matched RL setting cannot be printed as a difference.
3. **Contrast claims are typed.** `095_claims` gets kind `contrast` with fields property, group, contrast group. `checks.py` fails the build if the contrast group has the same code. The draft prints contrasts only through these claims or facts.
4. **A contrast lens in every review round.** For each statement "in settings G, P", the finder checks P in the matched RL setting. Add the class to the gate rule: "a claimed difference that the matched RL setting shares is a wrong fact".
5. **Key claims as contrasts.** Rewrite K01–K04 as matched contrasts; a one-sided key claim is not admitted.
6. **Audit 070.** Mark rows A1, B1, B2, C2, E2, E3 as phase-confounded or re-state them per phase; they stay unprinted until then.
7. **Test.** Property-based test in `test_analyze.py`: for random code tables, no difference fact names a property on which a setting equals its matched RL setting.

## Result (implemented, 2026-11-25)

| Part | Where | State |
|---|---|---|
| 23 coded properties × 9 settings, two independent Sonnet raters | `064_properties`, `066_property_codes` | 197/207 agree, kappa 0.92; rest adjudicated |
| 15 declared matched pairs; attribution per property | `063_contrasts/pairs.csv`, `100_analysis/contrasts.py` | R2 and P1 attribute to phase only: the original error now computes correctly |
| Typed contrast claims | `095_claims` (kind contrast) | checked by the build |
| Sentence-level linter: Haiku extracts every comparative claim per paragraph; Sonnet adjudicates each failing claim (mapping error or real); the build checks the result against the codes | `300_render/contrast_lint.py`, cache `contrast_lint.json` | build makes no model call; a changed paragraph or prompt re-lints |
| Overrides need a decision id | `300_render/contrast_overrides.csv` | 1 override (D17) |
| Contrast rule in finder, scorer and gate briefs | `096_review/briefs/` | gate rule stored once in `gate_brief.md` |
| Tests | `test_contrasts.py`, `test_contrast_lint.py` | 20 + 23 + 4 pass |

### What the linter found

- First run (prompt v1): 36 failures, mostly similarity and framing sentences read as differences. Prompt v2 adds a relation (differ, same, varies_within, general): 22 failures, none of them phase confounds.
- Sonnet adjudication of the 22: 20 mapping errors, 1 real, 1 parse error (the adjudicator returned lists of properties; parser fixed, test first).
- Real defects fixed as logged changes (`096_review/changes/round_2.csv` rows 40–46):
  1. "In the agent settings … the transition is what the tool and the world do, which no party fully controls" was false for agent training (T2 known: the designer builds and resets the sandbox). Now split by phase.
  2. "The other treats the inside as unknown …" read as "LLM work has no reward". Now states that it posits a reward to train, none for the task at deployment.
  3. Key claim K03 ("closest to RL training on dense reward, Markov prefix, known dynamics, free resets") was refuted by the codes: T-RL is partly Markov (POMDP), T-PRM yes; known dynamics and resets hold in every LLM training setting. K03 revised under D17; the prose now imports the computed fact `prm_like_rl` (reward at every step, episode has one action, further decision after an action, value estimate selects actions).
- Defect 3 was found only after the adjudicator split a multi-property claim that the Haiku pass had left unchecked (property null). A typed list of properties in prose is a fact the draft must import, not type (000_METHOD.md 1.1).

### Remaining risk

- The linter can miss a comparative sentence entirely (recall is not measured). The contrast lens in each review round is the second line.
- Adjudication verdicts are model judgements; the build trusts them. The cached verdicts and reasons are in `contrast_lint.json` for audit.
