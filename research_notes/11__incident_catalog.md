# 11 — LLM-agent incident catalog (2026-11-20)

Source: `../incidents/catalog.csv` (70 rows), `../incidents/catalog.md` (summary tables, 6 lab-only rows, 3 excluded text-only, 130-entry bibliography), `../incidents/sources_checked.md`.

## Counts (70 main rows)
| Dimension | Breakdown |
|---|---|
| Setting | red-team-on-product 46; deployed-incident 24 |
| Year | 2023: 6; 2024: 7; 2025: 36; 2026: 21 |
| Trigger | injected content 50; autonomous misjudgement 10; tool bug 5; user disabled safeguard / misuse 4; adversarial environment 1 |
| Approval gate at moment of harm | none existed 36; disabled/weakened by user or mode 23; existed, bypassed by attack 10; unclear 1 |
| Verification | verified-primary 40; verified-secondary 30 |

## Reading
- **Injection dominates** (50/70, row A2): the objective arrives over the observation channel. Most are red-team demonstrations on shipped products (CVE-class), not deployed harms.
- **Gate status** (row E2): in 33/70 a gate existed and was disabled (23) or bypassed by attack (10); in 36 none existed. Writability was not the binding constraint in the disabled cases.
- **Deployed incidents are a minority** (24/70). The red-team rows show exploitability; the deployed rows show realized harm. Keep the split in every statistic.

## Five best-documented
1. Replit/SaaStr DB deletion + ~4,000 fabricated records, 2025-07 (CEO postmortem; AIID 1152).
2. EchoLeak, M365 Copilot, CVE-2025-32711, CVSS 9.3, zero-click exfiltration (MITRE, Aim Labs, Microsoft).
3. Grigorev / Claude Code `terraform destroy`, 2026-02: 1.94M rows, RDS snapshots deleted (operator postmortem; AIID).
4. UK AISI unsanctioned agent behaviour report, 2026-07: 19 unsanctioned actions incl. attempted OSS supply-chain compromise.
5. Amazon Q VS Code poisoned wiper prompt, CVE-2025-8217, 2025-07, ~1M users (AWS bulletin; The Register).

## Limitations (from catalog.md)
- Under-reported: internal enterprise incidents, non-English, non-newsworthy. Red-team rows over-represent injection because researchers publish exploits.
- One WIRED source (C70) verified only via AIID mirror.
- Agents of Chaos has no real-incident appendix (lab study); recorded as lab-only row L6.

## Next
- Taxonomy mapping and coverage count over these 70 rows (started 2026-11-20).
