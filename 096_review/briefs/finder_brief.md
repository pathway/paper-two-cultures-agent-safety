QUESTION
Which statements in this position paper are factually wrong, overclaimed, or contradicted by its own tables or its cited sources? The answer decides what the next review round fixes.

SCOPE
- Rendered paper with numbers expanded: 300_render/out/paper.tex
- Source tables the paper is generated from: 060_settings/settings.csv, 062_primitives/primitives.csv, 065_primitive_cells/cells.csv, 085_breiman/cultures.csv; computed facts 100_analysis/facts.json; census snapshots 080_census/metrics.json and 080_census/general/metrics.json
- Verbatim extracts from the target texts, with locators: 047_extracts/<key>/extracts.csv and candidates.csv (sutton2018, mclean2026, breiman2001); the full texts in 045_fulltext/<key>.txt
- Frozen key of core claims: 096_review/key.csv
- Decisions already taken: 005_decisions/decisions.csv
- Matched contrasts (D15): 063_contrasts/pairs.csv, 064_properties/properties.csv, 066_property_codes/codes.csv; every comparative claim the linter found, with its check result: 300_render/out/contrasts.md

CONTRACTS
- Every quote must appear verbatim in the stored full text of the source cited next to it.
- Every sentence citing a work must be supported by that work as worded.
- Counts and shares in the prose must equal those the tables produce (100_analysis/facts.json).
- A table cell's value must be supported by its reason and sources; a cell marked as a quotation must quote the source.
- Grading rule for the primitive cells: the cell names what the primitive denotes in the setting as usually run; the reason gives the sources.
- Scope rule (D13): a true sentence or citation that serves no key claim or part of the scope line is a defect (orphaned); see 096_review/briefs/scope_brief.md.
- Contrast rule (D15): a sentence that says something holds in some settings and not in others must compare settings of the same phase (training with training, deployment with deployment), and the coded property must differ between the two groups. A claimed RL-versus-LLM difference that the same-phase RL setting shares is a wrong fact; a training-versus-deployment difference attributed to culture is a wrong fact.
- Numbers marked [U] are model-judged labels, declared unaudited; do not report that they are unaudited, report only if they are miscomputed or misdescribed.

ALREADY CHECKED
- 096_review/rejected.csv lists findings already judged and settled. Do not report them or rephrasings of them.
- Design choices recorded in 005_decisions/decisions.csv are settled unless a source contradicts them.

NOT IN SCOPE
Style, length, page limit, minor wording, LaTeX layout.

ASK
Read the paper in full, then check the quotes, cells, counts and internal consistency against the files. Report only material defects: a wrong fact or quote, a citation that does not support its sentence, a count or cell the sources do not support, a contradiction between two parts of the paper, or a missing qualification that changes a key claim. A source described wrongly is a wrong fact and is material even when the claim it supports survives.
Return JSON: {"findings": [{"where": <section or table>, "claim": <the paper's words>, "problem": <what is wrong>, "evidence": <verbatim quote from a file, naming the file and line>, "severity": "wrong"|"overclaim"|"unsupported"|"unclear", "key": <K01..K16 or "none">, "fix": <smallest correct change, naming the stage file>}]}. If you find no material defect, return {"findings": []}.
