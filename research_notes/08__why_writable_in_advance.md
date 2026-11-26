# 08 — Why "could a pre-deployment rule have blocked it?" and what it does not test (2026-11-20)

## Why it was made central
- Operationalizes debunking-draft precondition P3 (unsafe set writable before deployment), the precondition CMDPs, shields and Safety Gym all require.
- Mirrors Breiman's seven-dimension simulation (goodness-of-fit does not reject until misfit is extreme).
- Yes/no per incident: measurable, auditable.

## What it actually tests
- Whether the first-order harmful action was enumerable in advance. Not whether anyone would write the rule, keep it on, or whether the agent's objective could be specified.
- A tool-layer question, not an agent question. Confirmed by the result: `yes` rules are access control, not policy costs.

## Weaknesses
- Hindsight bias: given the incident, a rule can nearly always be written. 86% is an upper bound on foresight.
- Ill-posed for misuse: all 14 `no` are attacker-operated agents.
- Does not separate the cultures: both endorse "block destructive ops without approval" (shield vs least privilege).

## Better questions for the two-cultures claim
1. Which layer does the safety live in, and what residual remains after tool-layer rules (concealment, intent-indistinguishable misuse, legitimate-looking injections)? Rule-kind classification requested.
2. Was a gate present, and was it on? Row E2; where the headline cases failed.
3. Which culture's taxonomy fits? McLean's three classes vs the broader taxonomy with a "none fits" code (taxonomy agent).
4. Could the harm have been predicted from the stated objective? Tests the objective culture's own claim; not yet measured.

## Verdict
- Keep as one row of evidence about where specification lives. Do not present it as the paper's test of the two cultures; use the residual analysis and gate-status count for that.
