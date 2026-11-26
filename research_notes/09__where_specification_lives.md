# 09 — Operator split and where the writable specification lives (2026-11-20)

Source: `../coverage/coverage_report.md` section "Where the writable specification lives"; `../coverage/incidents_labeled.csv` columns `operator_type`, `rule_kinds`, `gate_bypassed`. 20 extra Haiku calls (123 total, ~USD 5.3).

## By operator type (Sonnet label)

| | Deployer-operated (N=64) | Attacker-operated (N=35) |
|---|---|---|
| yes | 39 (0.61 [0.49, 0.72]) | 4 (0.11) |
| partial | 25 (0.39 [0.28, 0.51]) | 17 (0.49) |
| no | **0 (0.00 [0.00, 0.06])** | 14 (0.40) |
| yes + partial | 64 (1.00 [0.94, 1.00]) | 21 (0.60) |

- Unclear operator: 4. All 14 `no` are attacker-operated (confirmed).
- Caveat: Haiku filed some hijacked deployer agents as attacker-operated (AIXBT injected prompts, Amazon Q supply chain, Nx malware invoking users' agents), so deployer N=64 is a lower bound.
- Kappa on the deployer subset 0.39.

## Rule kind (Haiku over Sonnet rule_text, yes+partial N=89, multi-label)

| Kind | n | share |
|---|---|---|
| allow/deny-list | 69 | 0.78 |
| approval gate | 54 | 0.61 |
| least-privilege credential | 35 | 0.39 |
| egress / DLP | 31 | 0.35 |
| rate / volume / spend limit | 27 | 0.30 |
| sandbox / isolation | 27 | 0.30 |
| untrusted-content scan | 10 | 0.11 |
| **policy-level cost (CMDP-style)** | **1** | **0.01** |

- Tool-layer access control: 88/89 (0.99). Policy-level cost: 1/89, and that one is policy-only.
- Gate existed but was disabled, bypassed or auto-approved: 6/89 rule texts (0.07); Sonnet's `oversight-disabled-by-user` label on 16/103 incidents (0.16).

## Reading for the paper
1. For every deployer-operated incident, a tool-layer rule could have blocked the first-order harm. "The cost cannot be written" (debunking P3) is false at the tool layer and true at the policy layer: 1 of 89 writable rules is a cost over the agent's behavior.
2. The RL culture's instruments (CMDP costs over the policy) are absent from the rules that would have worked. The rules that would have worked are Saltzer–Schroeder access control, the security culture's instruments. Both cultures can call them shields; only one culture built them.
3. The residual is not writability but (a) attacker-operated misuse, where the question is ill-posed (14/35 `no`), (b) partial coverage of concealment and injection (25/64 deployer cases are only `partial`), and (c) gates present but switched off (16% of incidents).
4. Breiman analogue: Hoadley's score engineering, exactly. The black box runs in production inside constraints written at the boundary, not inside the box.

## Limitations
- LLM-judged labels, kappa 0.24–0.39; hindsight bias in "writable"; AIID newsworthiness bias; `no` dominated by misuse; audit sample (15) not yet checked by a human.
