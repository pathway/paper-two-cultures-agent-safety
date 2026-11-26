QUESTION
For each key claim assigned to you, does the paper as built support it, support it only with a qualification it does not state, or is it refuted by the sources and tables?

SCOPE
As in finder_brief.md: 300_render/out/paper.tex, the stage tables, 100_analysis/facts.json, 047_extracts and 045_fulltext for sutton2018, mclean2026 and breiman2001, and 096_review/key.csv.

RULES
- supported: the paper states the claim and the tables or stored sources bear it out as worded.
- qualify: the claim holds only with a qualification the paper does not state, or a number differs slightly from the computed fact.
- refuted: the sources or tables contradict the claim.
- A key claim that contrasts settings is supported only if it compares settings of the same phase and the codes in 066_property_codes/codes.csv differ between the groups (D15).
- Judge the paper as frozen now; do not propose rewrites beyond the smallest fix.
- Numbers marked [U] are model-judged and declared unaudited; score them against facts.json, not against your own reading of the incidents.

ASK
Return JSON: {"scores": [{"id": <K..>, "verdict": "supported"|"qualify"|"refuted", "evidence": <verbatim quote from paper.tex and from the table or source, with file and line>, "fix": <smallest change if not supported, else "">}]}.
