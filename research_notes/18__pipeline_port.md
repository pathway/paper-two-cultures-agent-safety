# 18. The paper as a generated pipeline (port of paper__debunking/000_METHOD.md)

Date: 2026-11-25. Instruction: "read this file and apply this method fully to this paper". Reframing instruction the same day: "The point of this paper is to help RL people understand, how does reward, policy, action, obs, transition differ in LLM-chatbots (no tools) and LLM-tool-agents?"

## What was built (Part 1)

- Stage folders 005–300 per the method; `000_README.md` lists them. Pre-pipeline files archived in `900_archive/pre_pipeline/`.
- Core table: `065_primitive_cells/cells.csv`, 8 primitives (Sutton & Barto definitions, `062`) × 9 settings (`060`: T-RL, T-CHAT, T-RLVR, T-PRM, T-AGENT, D-RL, D-CHAT, D-AGENT-A, D-AGENT-X). Settings align with the companion paper's T-/D- split (decision D3).
- Supporting tables: assumptions A1–F2 (`070`), incident catalog with web snapshots (`075`, `045_fulltext/web`), model-judged labels with rater and run id (`078`), census snapshot with hashes (`080`), Breiman's culture lines with extract ids (`085`).
- Sources: 164 references (`040`), 154 confirmed by `verify.py`, 2 manual; 138 full texts held (36 copied from the companion paper, the rest fetched from arXiv), plus Sutton & Barto (548 pp.), Breiman 2001 with discussants (33 pp.), McLean et al.
- Extracts: Sutton & Barto ch. 1, 3, 17 and Breiman by a Sonnet workflow (215 verbatim candidates); McLean by the Haiku CLI (57). Curated extracts cited by cells: sutton2018 e1–e17, breiman2001 b1–b12, mclean2026 e1–e27.
- Build: `300_render/build.py` passes all checks; 14-page PDF; 70 references cited. Tests: 26 pass across five suites.

## Headline facts the build computes (100_analysis/facts.json)

- All three LLM deployment settings: no reward at run time. T-CHAT and T-RLVR are bandits (no transition). D-RL vs D-AGENT-X: all eight primitives differ; D-CHAT vs D-AGENT-A: seven of eight.
- Incidents (N=70; unaudited): fit none of McLean's classes 56% (rater A) vs 29% (rater B), kappa on class fit 0.26; "no rule could have blocked" among deployer-operated: 0 of 50.
- Census: 0.13% / 0.23% cross-references; Louvain purity 0.92.

## Review loop (Part 2), round 1

- Key: `096_review/key.csv`, 14 claims K01–K14. Settled list seeded with two findings from the 2026-11-21 priority check.
- Snapshot `900_archive/rounds/before_round_1.tgz`.
- Measure: Sonnet workflow (4 scorer groups, 5 finder lenses; 23 findings, 7 claims scored qualify) + Codex finder on an inlined brief (11 findings). Collected: 41.
- Gate (41 Sonnet refuters): 37 confirmed material, 3 refuted, 1 confirmed minor. Main defects: Hoadley's scorecards described as black boxes with boundary constraints (they are interpretable models with constraints inside); the McLean "no longer used" quote applied beyond the PRM; "differ on N primitives" computed from label strings; the deployer-operated result stated as full blocking when 36% were "partial"; SWE-RL misdescribed as sandbox RL; "both raters" for a same-model stability check; Moskovitz and Bristow misdescribed in related work.
- Fix (one pass, tables first, 37 changes logged in `096_review/changes/round_1.csv`); K03, K04, K10 reworded in `key.csv` with `revised_in = round 1`. Then 25 judgement cells upgraded to quote cells from the cell-evidence proposals (35 of 72 cells now quote a stored source).
- Score (`scores/round_1.csv`): 7 of 14 supported as frozen; 8 changed; 13 accepted finder hits; not clean. Settled list grew to R6.
- Fix-check: Sonnet (7 agents over 62 change rows) and Codex over the same rows; repairs applied next.

## Deviations and open items

- Cells are mostly `judgement` (62 of 72); a forward extraction over the works the cells cite is running so that cells can be upgraded to quotes.
- Decisions D3, D4, D6, D7, D8 are "author to confirm".
- Model-judged labels remain unaudited; every number resting on them carries [U].
