# Do safe RL and LLM-agent safety cite each other? A citation census

*Data: OpenAlex API, retrieved 2026-11-20. Code: `census.py`. All tables: `census_tables.md`, `metrics.json`.*

Breiman [1] guessed that 98% of statisticians were in the data-modeling culture and 2% in the algorithmic one. This census replaces a guess of the same kind for agent safety with counts. Corpus A is the safe-RL / objective-modeling literature; corpus B is the LLM-agent-safety / behavior-modeling literature.

## Headline numbers

| measure | A (safe RL) | B (LLM-agent safety) |
|---|---|---|
| works | 883 | 729 |
| references (all) | 32,460 | 14,204 |
| references landing in own corpus | 2,622 (8.1%) | 1,052 (7.4%) |
| references landing in the other corpus | 41 (0.13%) | 33 (0.23%) |
| cross share of in-corpus references | 41 / 2,663 = 1.5% | 33 / 1,085 = 3.0% |
| papers citing at least one work of the other corpus | 28 / 883 (3.2%) | 26 / 729 (3.6%) |
| cross-citations after removing "reward hacking"-only works from A | 1 / 26,695 (0.004%) | 18 / 14,204 (0.13%) |
| authors (OpenAlex ids) | 3,056 | 2,080 |
| authors in both corpora | 44 (1.4% of A, 2.1% of B; Jaccard 0.009) | |
| distinct venues | 203 | 158 |
| venues in both corpora | 25 (Jaccard 0.074); among top-15 lists only arXiv, Zenodo, SSRN, IEEE Access | |
| Louvain communities vs A/B labels (998 connected nodes) | purity 0.923, NMI 0.42, cross-label edges 74 / 3,737 (2.0%) | |
| B works citing any of 5 canonical safe-RL works found in OpenAlex | 15 / 729 (2.1%); 12 of them cite only Amodei et al. 2016 [2] | |
| A works citing any of 5 canonical LLM-agent works | 24 / 883 (2.7%); all 24 are "reward hacking" matches | |
| bridge set (matched both query lists) | 4 works, all "reward hacking" + "alignment faking" | |

```
share of each corpus's references, by destination
A -> within A   ###.....................................  8.1%
A -> B          ........................................  0.13%
A -> elsewhere  #####################################...  91.8%
B -> within B   ###.....................................  7.4%
B -> A          ........................................  0.23%
B -> elsewhere  #####################################...  92.4%
```

## Method

1. Seed corpora by OpenAlex `title_and_abstract.search` [3], years 2012-2026, type article or preprint, English, primary topic field Computer Science or Engineering, top 200 by relevance per query, then keep works with at least 1 citation or year >= 2024. A: 7 queries ("safe reinforcement learning", "constrained Markov decision process", "constrained policy optimization", "shielding reinforcement learning", "safe exploration", "reward misspecification reinforcement learning", "reward hacking"). B: 11 queries ("LLM agent safety", "prompt injection", "indirect prompt injection", "jailbreak LLM agents", "agent red teaming", "alignment faking", "scheming language models", "AI control", "sycophancy language models", "agentic misalignment", "tool-use agent safety"). Dedup by OpenAlex id. Works matching both lists form the bridge set and are excluded from A and B.
2. Measures use only the `referenced_works`, `authorships` and `primary_location.source` fields of the seed works. No extra calls were needed for the graph. Community detection: Louvain (networkx 3.3, seed 0) on the undirected union citation graph restricted to works with at least one in-corpus edge.
3. Canonical works resolved by DOI through free single-entity lookups. Safety Gym (Ray, Achiam, Amodei 2019) is not in OpenAlex: title searches for the full title and for "Safety Gym" both return 0 hits, so it is excluded from the denominator (5 canonical works per side, not 6).
4. 26 billable searches, 0 failed calls, all responses cached.

## Results

**Cross-citation (2a).** 0.13% of A's references land in B and 0.23% of B's land in A; within-corpus shares are 8.1% and 7.4%, so a paper is 60-30 times more likely to cite its own corpus than the other. Of in-corpus references, 1.5% (A) and 3.0% (B) cross the line.

**Where the crossings come from.** 40 of the 41 A->B citations are made by works that matched "reward hacking"; the single other is AI Safety Gridworlds (2017) [4], which cites Low Impact AI (an "AI control" match). The top A->B targets are Alignment Faking [5] (19 citations), AI Control [6] (6) and Agentic Misalignment [7] (5). On the B side, 12 of the 33 B->A citations go to Concrete Problems in AI Safety [2] and 9 to Reasoning Models Don't Always Say What They Think [8] (a "reward hacking" match); only 6 go to works that are classical safe RL (CPO [9], Lyapunov safe RL, decentralized safe RL, robust CBF safe RL, safe exploration in continuous action spaces, one 2024 survey); the other 6 go to further "reward hacking" matches. So the measurable contact between the two literatures runs almost entirely through the term "reward hacking", which since 2024 names an RLHF/LLM phenomenon more often than a classical-RL one: "reward hacking"-only works are 144 of A's 289 works in 2026 and 0 of 7 in 2012.

**Author overlap (2b).** 44 of 5,092 distinct author ids appear in both corpora. The top bridging authors (Yaodong Yang 4+3 papers, Fabien Roger 2+2, Krishnamurthy Dvijotham 1+3, Dacheng Tao 3+1, Karthik Narasimhan 3+1, Rohin Shah 2+1) each have at most 7 papers across both. Papers with any bridging author: 39/883 in A, 37/729 in B.

**Venue overlap (2c).** A's top venues after arXiv are IEEE Robotics and Automation Letters, IEEE Transactions on Automatic Control, IEEE TNNLS, TMLR, IEEE Transactions on Smart Grid. B's are Zenodo (172 works, 165 of them uncited), SSRN, Research Square, PhilPapers. The venue sets share 25 names (Jaccard 0.074), and the shared ones are generic repositories (arXiv, Zenodo, SSRN, OSF, Preprints.org, Research Square) plus IEEE Access and Electronics. No shared peer-reviewed ML or security venue appears in either top-15 list.

**Community structure (2d).** Louvain finds 13 communities with purity 0.923 against the A/B labels and NMI 0.42. The two largest are pure: 346 A / 2 B (safe RL, CPO, safe exploration) and 0 A / 249 B (prompt injection). The one mixed community (164 A / 75 B) is the "reward hacking" + "alignment faking" + "AI control" cluster, which is the bridge topic. Cross-label edges are 74 of 3,737 (2.0%). The A/B labeling alone has modularity 0.39 (Louvain's own optimum is 0.59), so the keyword labels are a good but not optimal cut of the graph; the better cut separates reward-hacking/alignment work from both classical safe RL and prompt-injection security.

**Time series (2e).** B->A rate by year: 2023 0/645 (0.0%), 2024 1/1,245 (0.1%), 2025 7/3,212 (0.2%), 2026 25/8,344 (0.3%). The rate rises but stays below 0.3%, and the rise tracks the growth of the reward-hacking/alignment-faking subtopic, not of prompt-injection or agent-security work. A->B is 0 in every year before 2025, then 3/6,008 (2025) and 37/8,341 (2026), again from "reward hacking" matches.

**Canonical works (2f).** B works citing CPO [9]: 1; Shielding [10]: 2; Moldovan & Abbeel [11]: 0; Garcia & Fernandez survey [12]: 0; Concrete Problems [2]: 12. A works citing Greshake et al. [13]: 1; AgentDojo [14]: 0; Alignment Faking [5]: 19; AI Control [6]: 6; In-context Scheming [15]: 9. Concrete Problems is the only safe-RL-era work that B cites in any number, and it is an agenda paper rather than a method.

## Robustness

| variant | A | B | A->B | B->A | purity | NMI |
|---|---|---|---|---|---|---|
| primary | 883 | 729 | 41 / 32,460 (0.13%) | 33 / 14,204 (0.23%) | 0.923 | 0.42 |
| narrow queries (A: CPO, shielding, safe exploration MDP; B: indirect prompt injection, alignment faking, jailbreak LLM agents) | 154 | 296 | 0 / 5,537 (0.0%) | 0 / 4,818 (0.0%) | 1.000 | 0.56 |
| A without "reward hacking"-only works | 689 | 729 | 1 / 26,695 (0.004%) | 18 / 14,204 (0.13%) | 0.993 | 0.53 |
| cited >= 1 only | 703 | 351 | 33 / 28,530 (0.12%) | 15 / 10,356 (0.14%) | 0.938 | 0.42 |

The conclusion does not change under any variant. The narrower the queries, the cleaner the split: with the narrow sets there are zero cross-citations in either direction and zero cross-label edges.

## Limitations

- **Keyword seeding.** The corpora are the top 200 relevance hits per phrase, not the full literature ("safe reinforcement learning" alone has 833 title/abstract hits). Phrase matching admits applied CMDP work (wireless, smart grid) into A and governance essays into B. The field filter (Computer Science or Engineering) removed off-topic hits but will also have dropped some philosophy and social-science alignment work.
- **"Reward hacking" is a label shared by both cultures.** Assigning it to A was the design choice that produced nearly all measured contact. The sensitivity row above shows the result without it.
- **Coverage.** OpenAlex indexes arXiv but not OpenReview-only or lab-blog works; Safety Gym is absent, and most Anthropic/Redwood/Apollo reports exist only as arXiv records. OpenAlex reference lists for arXiv preprints are often incomplete, which lowers all in-corpus and cross-corpus counts alike; the shares, not the raw counts, are the robust quantity.
- **2026 skew and uncited long tail.** 509 of B's 729 works are from 2026 and 378 have zero citations; 165 of those are Zenodo uploads. The "cited >= 1 only" variant controls for this and gives the same answer.
- **Abstracts.** Search quality depends on OpenAlex having an abstract; this was not measured per work.
- **Author ids** are OpenAlex disambiguations; splits and merges will shift the 44 count by a few either way.

## What this means for the two-cultures claim

The split is visible in the citation graph independent of the keyword labels: the largest Louvain community is 99% safe RL, the second is 100% prompt-injection work, and only 2% of in-corpus edges cross the labels. Shared authors (under 2%) and shared venues (only general repositories) tell the same story. Breiman's 98/2 was a guess about headcount; the measured quantity here is contact, and it is below 0.3% of references in both directions.

Two qualifications belong in the paper. First, the cultures are not symmetric in size or age: A spans 2012-2026 with 203 venues, B is 94% (687/729) 2024-2026 works. Second, the one place the cultures touch is "reward hacking", where the RL vocabulary (Amodei et al. 2016 [2], CPO-era objective language) is reused to describe LLM training failures; this is the seam where McLean-style "internalized reward" reasoning enters the LLM literature, and the census locates it precisely.

## Bibliography

1. Breiman, L. (2001). Statistical Modeling: The Two Cultures. *Statistical Science* 16(3). https://doi.org/10.1214/ss/1009213726 (OpenAlex W2084341220)
2. Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., Mané, D. (2016). Concrete Problems in AI Safety. arXiv:1606.06565. https://doi.org/10.48550/arXiv.1606.06565 (OpenAlex https://openalex.org/W2462906003)
3. OpenAlex. Works API, `title_and_abstract.search` filter and pricing. https://help.openalex.org/api/searching/ and https://help.openalex.org/access/example-costs/
4. Leike, J., Martic, M., Krakovna, V., et al. (2017). AI Safety Gridworlds. arXiv:1711.09883. https://doi.org/10.48550/arXiv.1711.09883 (OpenAlex https://openalex.org/W2768908787)
5. Greenblatt, R., Denison, C., Wright, B., et al. (2024). Alignment faking in large language models. arXiv:2412.14093. https://doi.org/10.48550/arXiv.2412.14093 (OpenAlex https://openalex.org/W4405627013)
6. Greenblatt, R., Shlegeris, B., Sachan, K., Roger, F. (2023). AI Control: Improving Safety Despite Intentional Subversion. arXiv:2312.06942. https://doi.org/10.48550/arXiv.2312.06942 (OpenAlex https://openalex.org/W4389714039)
7. Lynch, A., et al. (2025). Agentic Misalignment: How LLMs Could Be Insider Threats. arXiv:2510.05179. https://doi.org/10.48550/arXiv.2510.05179 (OpenAlex https://openalex.org/W4414973934)
8. Chen, Y., et al. (2025). Reasoning Models Don't Always Say What They Think. arXiv:2505.05410. https://doi.org/10.48550/arXiv.2505.05410 (OpenAlex https://openalex.org/W4416091752)
9. Achiam, J., Held, D., Tamar, A., Abbeel, P. (2017). Constrained Policy Optimization. arXiv:1705.10528. https://doi.org/10.48550/arXiv.1705.10528 (OpenAlex https://openalex.org/W2616964725)
10. Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S., Topcu, U. (2018). Safe Reinforcement Learning via Shielding. arXiv:1708.08611. https://doi.org/10.48550/arXiv.1708.08611 (OpenAlex https://openalex.org/W2751422670)
11. Moldovan, T. M., Abbeel, P. (2012). Safe Exploration in Markov Decision Processes. arXiv:1205.4810. https://doi.org/10.48550/arXiv.1205.4810 (OpenAlex https://openalex.org/W2151237105)
12. García, J., Fernández, F. (2015). A comprehensive survey on safe reinforcement learning. *JMLR* 16. https://jmlr.csail.mit.edu/papers/volume16/garcia15a/garcia15a.pdf (OpenAlex https://openalex.org/W1845972764)
13. Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., Fritz, M. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. arXiv:2302.12173. https://doi.org/10.48550/arXiv.2302.12173 (OpenAlex https://openalex.org/W4388886073)
14. Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., Tramèr, F. (2024). AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. arXiv:2406.13352. https://doi.org/10.48550/arXiv.2406.13352 (OpenAlex https://openalex.org/W7128378279)
15. Meinke, A., Schoen, B., Scheurer, J., Balesni, M., Shah, R., Hobbhahn, M. (2024). Frontier Models are Capable of In-context Scheming. arXiv:2412.04984. https://doi.org/10.48550/arXiv.2412.04984 (OpenAlex https://openalex.org/W4405173927)

Bridge-set works (all four matched "reward hacking" and "alignment faking"): https://openalex.org/W7106695004, https://openalex.org/W7141222905, https://openalex.org/W7222945718, https://openalex.org/W7212077014. Not in OpenAlex: Ray, Achiam, Amodei (2019) Benchmarking Safe Exploration in Deep Reinforcement Learning (Safety Gym).
