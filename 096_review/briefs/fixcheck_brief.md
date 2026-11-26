QUESTION
A review round applied the changes listed in 096_review/changes/round_1.csv (columns: change, finding_ids, file, old, new, source_quote). For each change row, is the new text correct and consistent, or did the fix break something?

CONTRACTS
- A quoted phrase in the new text must be verbatim in the stored full text of the cited work; the attached extracts show the verbatim passages held for the target texts (full texts not attached: if a quote is not in the attached extracts, say "cannot check" rather than "broken").
- The cited work must support the sentence as worded.
- Counts in prose must match 100_analysis/facts.json.
- The new text must not contradict another part of the paper or the tables.

ASK
All files are attached below this brief; you cannot read the file system. Output ONLY JSON lines, one per change row, with keys "change" (integer), "status" ("ok"|"broken"|"cannot check"), "reason", "repair" (exact repair text and file if broken, else ""). Do not run shell commands.
