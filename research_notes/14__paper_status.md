# 14 — Paper status (2026-11-20, end of day)

## Thesis after the pivot
- Two cultures are real: within-corpus citation ~50× more likely than cross-corpus; the one bridge is "reward hacking" (06).
- "Assume the agent maximizes R" does not describe deployed incidents: McLean's 3 classes have no slot for 47%; the assigned class is unstable (kappa 0.25) while facts are stable (0.86–0.90) (13).
- Written constraints work, but live in the tool layer: deployer-operated `no` = 0/113 across two sources; 1/154 writable rules is a policy-level cost; all 70 incidents coded to runtime control (area 10), none to formal guarantees or specification (09, 12, 13).
- Residual: concealment, legitimate-looking injection, misuse, gates switched off (07, 09, 11).
- Breiman analogue: Hoadley's score engineering, not "goodness-of-fit has no power" (07).

## Evidence
| Measurement | N | Status |
|---|---|---|
| Citation census | 883 + 729 | done |
| Coverage count | 148 (AIID + catalog, dedup) | done, model-judged |
| Incident catalog | 70 verified | done |
| Taxonomy mapping, 24 dims incl. cannon unified taxonomy | 70 | done, Haiku |
| Related work | 31 verified cites | done; no pre-emption |

## Strong
- Four mutually consistent measurements from two independent incident sets; central table backed by counts; novel, replicable instability finding; honest pivot.

## Weak
- All labels model-judged, zero human-checked; headline kappa 0.24–0.41. Biggest risk; fixable with the 15-item audit.
- Catalog 2/3 red-team rows; injection partly an artefact of publication.
- Small N; Agent Incident Registry (~500) unused.
- Three agent-incident databases exist; catalog is not a contribution alone.
- No draft text yet.

## Readiness
- Draftable now: intro, census, table, coverage, taxonomy, final remarks. No number in print before the audit.
- Venue: position track or discussion journal; 15–25 pages.

## Recommended next
1. Human audit of coverage/human_check_sample.md.
2. Run coverage + taxonomy over the Agent Incident Registry (~150–250 Haiku calls).
3. Draft from framing.md and notes 01–13 with number placeholders.
