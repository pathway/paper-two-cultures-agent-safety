# 21. Orphaned units: sentences that outlive the scope that needed them

Trigger (author, 2026-11-25): "Bristow et al. (2023) call the ethics-versus-alignment split a caricature of binary camps -- is this relevant to our topic??? … If not, think how that got in there, then review the WHOLE paper for such more generally."

## Answer
Not relevant. Bristow et al. [1] treat AI ethics versus AI alignment (a pause letter, rogue agents, bridges between camps); the stored full text mentions agents 4 times and RL not at all. Our sentence itself calls the split "orthogonal".

## Origin (traced)
1. `research_notes/03__related_two_cultures_findings.md`: the then title "Two cultures of AI safety" collided with an existing usage (ethics vs safety; Bristow et al. 2023 and others). The intro had to say our split is a different one. The sentence was a name disambiguation.
2. `research_notes/15__twopager_v0.1.md`: moved into related work.
3. Round 1 (`096_review/changes/round_1.csv` row 22): a finder showed the sentence misdescribed Bristow; the fix made it faithful. The question asked was "is it true?", never "why is it here?".
4. D9 re-scope: removed sentences that name safety. This one names no safety topic, so it survived, although its only reason (the old title) was gone.

## The class
A unit (sentence, citation, caption, statement, reference) is **orphaned** when it is true but serves no key claim, primitive, setting, fact, the cultures frame, the census, an objection, or the scope line. No check caught it: the build checks facts, the review checks truth. Nothing checked relevance to D13.

## Removal
1. Whole-paper scope review now (Sonnet: 7 finders by section and bibliography, then a refuting gate; Codex in parallel), brief `096_review/briefs/scope_brief.md`.
2. Scope rule added to `finder_brief.md` and `gate_brief.md`: an orphaned unit is material.
3. Planned: a `role` field per cited reference naming the key claim or scope part it serves; the build fails on a cited reference without a role or whose role names no existing key id or scope part. A re-scope then forces every role to be re-read.

## Bibliography
[1] T. Bristow, L. Thorburn, D. Acosta-Navas, "Views on AI aren't binary, they're plural," arXiv:2312.14230, 2023. https://arxiv.org/abs/2312.14230

## Whole-paper review result (2026-11-25)
Sonnet: 7 finders, 53 units flagged, gate confirmed 38, refuted 13, settled 2. Codex: 18 units, most overlapping. Findings: `096_review/findings/scope_round_2_sonnet.json`, `096_review/codex/scope_round_2.jsonl`.

| Cluster | Removed | Origin |
|---|---|---|
| S1 bridge proposal | Hoadley score-engineering analogy, "constraints sit in the scaffold", conclusion's "run inside written constraints"; K08 drops Hoadley (D19) | round-1 "engineer the boundary" recommendation; violates D13 |
| S2 safety-era related work | Bristow, Çağatan, "RL safety tools / conditions those tools need", Shmueli, Donoho, Efron 2020, Gao 2023 | notes 03, 15 |
| S3 PRM practice | DeepSeek-R1 dropping a PRM; Zhang 2025 PRM quality | pre-rescope draft |
| S4 safety census sentence | second census on safety sub-literatures | safety version; K11 covers the general census only |
| S5 D-AGENT-X cell reasons | Baker 2025 test gaming; duplicated Greshake quote; Chan 2023 | safety-era cells |
| S6 dead claims | caption_census, caption_coverage, caption_incidents, set_incidents, set_deployer, caption_assumptions | D9 leftovers, unprinted but stamped |
| S7 keyword | "AI safety" | safety title |

Kept on the author's approval of the recommendation: Turner 2022 (bears on what reward means for a trained policy; the gate's refutation cited a sentence that does not cite Turner, so the gate erred), Moskovitz 2024 and Korbak 2022 (readings of the RLHF reward), D'Amour 2021 (Rashomon, cultures frame).

Gate error worth recording: one refutation cited evidence that does not exist (Turner "used at draft line 55"). A gate verdict needs a check that its cited location contains the cited key.
