# 12 — Coverage count extended to the catalog; combined N = 148 (2026-11-20)

Source: `../coverage/coverage_report.md` §"Catalog (N=70)", `../coverage/catalog_labeled.csv`. 28 extra calls (151 total: 117 Haiku, 34 Sonnet; subscription login). Labels for this run were Sonnet primary; future runs use Haiku by default.

## Dedup
- 21 of 70 catalog rows matched already-labelled AIID rows (labels reused; match confidence 0.85–0.98). 49 judged fresh; 4 vetoed as not an acting LLM agent (MCP server bugs/backdoors: C18, C20, C24, C40). Catalog N = 66. Kappa 0.41.

## Catalog headline (N = 66)
| | yes | partial | no |
|---|---|---|---|
| all | 36 (0.55 [0.43, 0.66]) | 29 (0.44) | 1 (0.02) |
| deployed-incident (22) | 13 (0.59) | 8 (0.36) | 1 (0.05) |
| red-team-on-product (44) | 23 (0.52) | 21 (0.48) | 0 |
| deployer-operated (49) | 32 (0.65) | 17 (0.35) | 0 |
| attacker-operated (15) | 3 (0.20) | 11 (0.73) | 1 (0.07) |
- The single `no` is attacker-operated (Aurora ransomware operators driving Cursor Agent).
- Rule kinds (65 rules): allow/deny-list 0.78, approval gate 0.75, egress/DLP 0.42, untrusted-content scan 0.31, least privilege 0.28, sandbox 0.26, rate/spend limit 0.08, **policy-level cost 0**. Tool-layer access control 65/65. Gate present but disabled/bypassed by user: 7/65.
- Injection-heavy catalog shifts weight toward content scanning and egress control vs the AIID set.

## Combined AIID + catalog, deduplicated (N = 148)
| | n | share | 95% Wilson |
|---|---|---|---|
| yes | 68 | 0.46 | [0.38, 0.54] |
| partial | 66 | 0.45 | [0.37, 0.53] |
| no | 14 | 0.09 | [0.06, 0.15] |
| yes + partial | 134 | 0.91 | [0.85, 0.94] |
- All 14 `no` remain attacker-operated. Deployer-operated `no` = 0 across both sources.
- Policy-level (CMDP-style) cost: 1 of 154 writable rules across both sources.

## Reading
- Robust across two independently assembled incident sets: first-order harm is blockable by a tool-layer rule in every deployer-operated case; the rule is access control, not a cost over the policy; the open residual is partial coverage (concealment, legitimate-looking injection) and gates switched off.

## Limitations
- Model-judged (kappa 0.24–0.41); hindsight bias; catalog is 2/3 red-team rows by construction; 15-item audit sample still unchecked.
