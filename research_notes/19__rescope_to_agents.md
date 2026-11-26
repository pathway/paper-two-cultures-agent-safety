# 19. Re-scope: from agent safety to the two cultures of agents

Date: 2026-11-25. Decisions D9, D12, D13, D14 (`005_decisions/decisions.csv`).

## Author's instructions
- "I wanted a two_cultures_of_agents, not about safety per se."
- "7. What the incidents say -- this does not belong in this paper at all."
- "Classical-RL default / LLM-agent default -- false dichotomy; in RL you can also have deployed policies."
- "TWO CULTURES UNDERSTAND AGENT VERY DIFFERENTLY, this paper examines the gap." "Only describe the gap for now."
- "Follow the pipeline process."

## Scope line (stamped claim `scope_purpose`, version 1 chosen by the author)
When an RL researcher and an LLM-agent builder say *agent*, they name different objects, and claims that cross between them arrive with the words but not the objects: a deployed LLM agent is said to hack a reward it does not have. This paper lays the two meanings side by side, one primitive at a time, in training and in deployment, and says where each word keeps its meaning and where it loses it. It describes the gap and proposes no bridge.

## What changed (all logged in `096_review/changes/rescope_D9.csv`)
- Draft rewritten for the scope; incident, coverage and safety-residual sections removed; assumptions table not printed; RL read as T-RL and D-RL.
- Key: K09, K10, K12 removed; K03, K04, K11, K13 revised; K15 (scope) added.
- New general census (`080_census/general`, D11, D14): RL-agent corpus 1117 works, LLM-agent corpus 703; 3 of 52,183 RL references and 50 of 22,865 LLM-agent references cross; Louvain purity 0.98.
- Snapshots: `900_archive/rounds/before_rescope.tgz`, `before_round_2.tgz`; pre-rescope draft in `900_archive/draft_safety_prerescope_2026-11-25.md`.

## Process error recorded
- I first rewrote the draft without snapshot, log or key revision. The author stopped it. The draft was restored and the change re-applied through the stages in order.

## Open
- D10: whether paper__debunking takes the incident results is the author's call; nothing there was edited.
- Round 2 review (both model families) running on the re-scoped paper.
