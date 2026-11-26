QUESTION
Does every sentence, citation, caption, statement and bibliography entry of the paper serve its stated scope? The answer decides what the next fix removes or rewrites.

SCOPE LINE (095_claims/claims.csv, scope_purpose; decision D13)
When an RL researcher and an LLM-agent builder say *agent*, they name different objects. The paper lays the two meanings side by side, one primitive at a time (reward, policy, action, observation, state, transition, episode, value), in training and in deployment, and says where each word keeps its meaning and where it loses it. It describes the gap and proposes no bridge.

DECIDED OUT OF SCOPE
- Safety as a topic: incidents, coverage of safety tools, guarantees, conditions for RL safety methods (D9, D10; the companion paper owns them).
- Any bridge or proposal (D13).
- A "classical-RL default vs LLM-agent default" opposition (D12).

WHAT SERVES THE SCOPE
A unit serves the scope if it does at least one of: states or supports a key claim in 096_review/key.csv; defines or explains a primitive or setting; gives evidence for a cell, a code or a computed fact; states the cultures frame (Breiman) the paper uses to name the gap; shows how far the two literatures read each other (census); answers an objection to the paper's own claims; states the scope or the limits of the paper.

DEFECT CLASS: ORPHANED UNIT
A unit is orphaned when it is true but supports nothing above. Typical origin: it was written for an earlier scope (the paper was "Two Cultures of Agent Safety" until D9) and survived because it does not name the dropped topic. Examples of the pattern: a sentence that disambiguates the paper's name from another literature that only shared the old name; a citation kept only for a sentence of that kind; a caveat about a claim the paper no longer makes; a statement (impact, disclosure) written for the safety version.

ASK
For each unit you judge, return: where (section, first words), unit (sentence, citation, caption, statement, reference), verdict (serves | orphaned | off_scope | unclear), serves (key id, primitive, setting, fact, or the scope part it serves; empty if none), origin (why you think it is there; cite research_notes/ or 900_archive/ if you find it), fix (delete, or the exact shorter text). Report only orphaned, off_scope and unclear units; do not list units that serve the scope. Style and length are out of scope.
