QUESTION
Is this review finding a real, material defect of the paper as built? The verdict decides whether the fixer acts on it.

SCOPE
300_render/out/paper.tex; the stage files the finding names; 100_analysis/facts.json; 300_render/out/contrasts.md; the stored sources (047_extracts, 045_fulltext); 096_review/rejected.csv; 005_decisions/decisions.csv.

RULES
- Try to REFUTE the finding from the stage files and stored sources.
- settled: a decision or a rejected.csv row covers it. refuted: the paper and sources do not bear it out. confirmed: otherwise.
- material: a wrong fact or quote, an unsupporting citation, a wrong count or cell, a contradiction, or a missing qualification that changes a key claim.
- A source described wrongly is a wrong fact and is material even when the claim it supports survives.
- A unit that is true but serves no key claim, primitive, setting, fact, the cultures frame, the census, an objection or the scope line is material: it is off scope (scope_brief.md).
- A claimed difference between settings that the same-phase comparison setting shares is a wrong fact (D15). A training-versus-deployment difference attributed to culture is a wrong fact (D15).

ASK
Return JSON: {"verdict": "confirmed"|"refuted"|"settled", "material": true|false, "reason": <one or two sentences>, "source_file": <file and line of the evidence>, "fix": <smallest correct change, stage file first, exact text>}.
