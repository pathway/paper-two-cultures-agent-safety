# 13 — Taxonomy mapping of the 70-row catalog, incl. the unified taxonomy (2026-11-20)

Source: `../taxonomy/taxonomy_stats.md`, `../taxonomy/labels.json`. Haiku primary on 24 dimensions; Haiku with reworded prompt as second rater on D6, D8, D9b. 28 calls, subscription. 20 validation problems (judge emitted non-existent code ids, e.g. `D4b.privilege_compromise`; those cells dropped, no rerun).

## Headline (N = 70)
| Code | k/N | Share | Wilson 95% |
|---|---|---|---|
| McLean: none of the three fits | 33/70 | 47% | 36–59% |
| McLean: insufficient observation | 26/70 | 37% | |
| McLean: reward misspecification | 7/70 | 10% | |
| McLean: unsafe action in irreversible state | 3/70 | 4% | |
| Trigger = injected content (row A2) | 50/70 | 71% | 60–81% |
| Human gate present but bypassed or disabled (row E2) | 24/70 | 34% | 24–46% |
| Concealment present | 10/70 | 14% | |
| Irreversible | 35/70 | 50% | |
| Severity major / near-miss | 22 / 48 | 31% / 69% | |

## McLean class × trigger
- Of 50 injection incidents: 28 none_fits, 20 insufficient_observation, 2 reward_misspecification. The RL taxonomy either has no slot for injection or files it as "bad observation", which hides that the observation rewrote the objective.
- Reward misspecification (the RL culture's flagship class) covers 7/70, mostly autonomous misjudgement.

## Assumption rows most often broken (D7, multi-label)
- C4 adversarial environment 71%; D1 open action space 71%; A2 objective via observation channel 69%; D3 steerable without retraining 50%; F1 safety measured by incidents 41%; A1 30%; C1 nobody built the environment 29%; E2 human in loop 26%; B1 frozen policy 24%; C2 single-shot 23%; E1 agent models overseer 17%.
- Rarely broken: A4 preference steering 1%, B2 2%, A5 unwritable unsafe set 9%. Consistent with the coverage result: writability is not the binding constraint.

## Unified taxonomy (cannon), problem side (D9a)
- 4.3 Adversarial inputs, jailbreaks, injection 70%; 5.5 Loss of control 46%; 1.2 Cyber offence 31%; 2.2 Privacy 26%; 4.1 Distribution shift / goal misgeneralisation 11%; 3.2 Side effects 10%; 3.1 Reward hacking / Goodhart 9%; 4.2 Safe exploration 3%; 5.1 Deception/scheming 3%.
- The RL-native problem areas (3.1, 3.2, 4.2) together cover ≤ 20% of incidents; the security-native area (4.3) covers 70%.

## Unified taxonomy, response side that would have prevented or caught it (D9b)
- 10.3 Safeguards, access restriction **86%**; 10.2 Monitoring 63%; 7.4 Red teaming 41%; 10.1 Control protocols / human oversight 29%; 10.5 Security, provenance, tracking 26%; 10.4 Intervention 10%; 9.2 Scalable oversight 7%; 11.2 Safer design patterns 7%; **11.1 Formal guarantees 0%**; **3.x specification work 0%** (not offered as a response area in the tree; 9.4 specs/constitutions 1%).
- Area 10 (Control, monitoring, runtime defence) dominates. Area 11 (safe by design and theory) and area 9 (training) are near zero. The two-cultures reading: the response that fits real incidents is the behavior culture's runtime control at the tool layer, not the objective culture's specification or guarantees.

## Agreement (prompt stability, Haiku vs Haiku reworded)
| Dim | kappa |
|---|---|
| D8a trigger | 0.90 |
| D8d human gate | 0.86 |
| D8f severity | 0.90 |
| D8c concealment | 0.61 |
| D8e harm type | 0.68 (per-code mean) |
| **D6 McLean class** | **0.25** |
| D8b irreversibility | 0.12 |
| D9b response sub-area | 0.11 (per-code mean; Jaccard 0.52) |
- Operational facts are stable. The McLean class is not: the reworded rater moved the first five injection cases from insufficient_observation to reward_misspecification. The RL class assignment is post hoc (debunking draft §7) and this is measurable evidence of it. D9b per-code kappa is low because of many sparse codes; at area level the pattern is stable: mean area-level Jaccard 0.78; **area 10 (runtime control) chosen by both raters for 70/70 incidents** (kappa undefined because unanimous); area 7 red-teaming kappa 0.69 (35 vs 34); area 9 training kappa 0.48 (8 vs 7); areas 8, 11, 12 too sparse (≤5) for a meaningful kappa.

## Limitations
- Judges read catalog rows, not primary sources; Haiku-only; 2/3 of rows are red-team demonstrations, which inflates injection and area 4.3; N = 70; single rater on D1–D5, D7, D9a; 20 dropped cells from invalid code ids.
