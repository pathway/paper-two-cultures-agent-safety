# 07 — Incident coverage count: results and a pivot in the claim (2026-11-20)

Source: `../coverage/coverage_report.md`, `../coverage/incidents_labeled.csv`. AI Incident Database snapshot 2026-11-16 (CC BY-SA 4.0) [1], plus 6 Agents of Chaos case studies [2] and 1 Greshake et al. demonstration [3].

## Funnel
- 1,282 AIID incidents dated ≥ 2023-01-01 → regex prefilter 649 (+7 supplementary) → Haiku stage 1: 140 agentic, 420 text-only LLM, 90 not LLM, 6 unclear → Sonnet veto of 37 non-agents → **N = 103 LLM-agent incidents**.
- 103 claude CLI calls (79 Haiku, 24 Sonnet), 0 errors, USD 4.89. Cached; rerun is free.

## Headline (Sonnet main rater, N = 103)

| Could a pre-deployment rule have blocked it? | n | share | 95% Wilson |
|---|---|---|---|
| yes | 44 | 0.43 | [0.34, 0.52] |
| partial (first-order harm blockable, rest not) | 45 | 0.44 | [0.35, 0.53] |
| no | 14 | 0.14 | [0.08, 0.22] |
| yes + partial | 89 | 0.86 | [0.78, 0.92] |

- Haiku second rater: yes 0.51 / partial 0.46 / no 0.03. Cohen's kappa 3-way 0.24 (raw 0.56). The `no` share is rater-dependent (0.03–0.14).
- By failure type: irreversible-action-without-info has the highest yes-share (17/25); concealment/deception the lowest (1/15 yes, 14 partial); misspecification 41/77 yes.

## Two observations from the raw labels (my reading, 2026-11-20)
1. **Every `no` is an attacker-operated agent** (Xanthorox, 007TG, Hermes, ARTEX, state-linked intrusions, Cursor used by a ransomware operator). No deployer existed to write a rule. Among deployer-operated agents the `no` count is 0 of 89.
2. **The `yes` rules are not cost functions over the policy.** Keyword counts over the 44 `yes` rule texts: approval 26, allowlist 24, deny 24, human 21, block 20, credential 17, sandbox 14, read-only 6. These are tool-layer access-control rules (least privilege, egress default-deny, approval gates on destructive or paying actions), i.e. Saltzer–Schroeder, not CMDP costs.

## Consequence: the paper's claim must pivot
- **Not supported as stated:** "specification-based safety has little coverage of real agent failures." First-order harm was blockable by a writable rule in 86% of incidents.
- **Supported, and more interesting:**
  a. The writable specification lives in the tool layer as access control, not in the agent's objective. Both cultures can claim it (RL: shield; security: least privilege). This is Hoadley's "score engineering" [4], and it is the hybrid the paper should recommend.
  b. The residual that no rule covers is concealment (14/15 only partial), intent-indistinguishable misuse (all 14 `no`), and injected instructions that look legitimate.
  c. Rules that existed were disabled or bypassed in several headline cases (Terraform/Claude Code skip-permissions; one `yes` rule literally reads "must not run with permission-bypass flags"). The binding constraint is human factors, row E2, not writability.
- Breiman analogue shifts: not "goodness-of-fit has no power" but Hoadley's reply to Breiman: black boxes work in production only inside written constraints that clients, law and drift demand.

## Limitations
- AIID newsworthiness bias; model-judged labels with low kappa on the 3-way label; hindsight bias in "writable in advance" (prompt guards against it, cannot remove it); `no` is dominated by misuse cases where the question is ill-posed.
- 15-incident human-check sample in `../coverage/human_check_sample.md`, not yet audited.

## Next
- Classify each yes/partial rule by kind (approval gate / allow-deny list / least-privilege credential / egress or DLP / rate or spend limit / content scan / policy-level cost) and split all stats by deployer-operated vs attacker-operated. Requested from the coverage agent 2026-11-20.
- Rerun over the full incident catalog when it lands.

[1] Responsible AI Collaborative, AI Incident Database, snapshot backup-20261116100722. https://incidentdatabase.ai/research/snapshots/
[2] Shapira et al., "Agents of Chaos," 2026. https://arxiv.org/abs/2602.20021
[3] K. Greshake et al., "Not What You've Signed Up For," AISec 2023. https://arxiv.org/abs/2302.12173
[4] B. Hoadley, Comment on Breiman, Statistical Science 16(3), 2001. https://doi.org/10.1214/ss/1009213726
