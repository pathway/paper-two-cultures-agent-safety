# Census tables

!!! warning "Status: STARTED"
    Draft. Not fully human-reviewed. See [the AI-use statement](../../ai-use.md).


Generated 2026-11-20 23:20 UTC. API failures recorded: 0.

## Corpus sizes

| set | works | total refs |
|---|---|---|
| A | 883 | 32460 |
| B | 729 | 14204 |
| bridge (matched both) | 4 | |

## 2a Cross-citation

| from | total refs | within corpus | cross corpus | cross/total | cross/in-corpus | papers citing other corpus |
|---|---|---|---|---|---|---|
| A -> B | 32460 | 2622 (8.1%) | 41 (0.1%) | 0.1% | 1.5% | 28 / 883 |
| B -> A | 14204 | 1052 (7.4%) | 33 (0.2%) | 0.2% | 3.0% | 26 / 729 |

```
A refs -> within A   ###..................................... 8.1%
A refs -> other       ........................................ 0.1%
A refs -> outside     #####################################... 91.8%
B refs -> within B   ###..................................... 7.4%
B refs -> other       ........................................ 0.2%
B refs -> outside     #####################################... 92.4%
```

## 2b Author overlap

- authors in A: 3056; in B: 2080; in both: 44 (1.4% of A authors, 2.1% of B authors; Jaccard 0.0086)
- papers with at least one bridging author: A 39/883, B 37/729

| bridging author | OpenAlex id | papers in A | papers in B |
|---|---|---|---|
| Yaodong Yang | https://openalex.org/A5090073634 | 4 | 3 |
| Fabien Roger | https://openalex.org/A5028042353 | 2 | 2 |
| Karthik Narasimhan | https://openalex.org/A5025205227 | 3 | 1 |
| Krishnamurthy Dvijotham | https://openalex.org/A5050954769 | 1 | 3 |
| Dacheng Tao | https://openalex.org/A5074103823 | 3 | 1 |
| Joe Benton | https://openalex.org/A5056010406 | 2 | 1 |
| Geoffrey Irving | https://openalex.org/A5029611587 | 1 | 2 |
| Francesco Belardinelli | https://openalex.org/A5055883955 | 2 | 1 |
| Subramanyam Sahoo | https://openalex.org/A5025127084 | 2 | 1 |
| Samuel R. Bowman | https://openalex.org/A5112713734 | 2 | 1 |
| Ethan Perez | https://openalex.org/A5091112967 | 1 | 2 |
| Rohin Shah | https://openalex.org/A5012971694 | 2 | 1 |
| Nathaniel Mitrani Hadida | https://openalex.org/A5123844931 | 1 | 2 |
| Aman R. Chadha | https://openalex.org/A5047032131 | 1 | 1 |
| Carson Denison | https://openalex.org/A5079864698 | 1 | 1 |
| Yongzhi Qi | https://openalex.org/A5148863082 | 1 | 1 |
| Mikita Balesni | https://openalex.org/A5092825639 | 1 | 1 |
| Jared Kaplan | https://openalex.org/A5053213601 | 1 | 1 |
| Sebastian Farquhar | https://openalex.org/A5051690066 | 1 | 1 |
| Tom Goldstein | https://openalex.org/A5060687985 | 1 | 1 |

## 2c Venue overlap

- distinct venues: A 203, B 158, shared 25; Jaccard(all) 0.0744; Jaccard(venues with >=2 papers) 0.0777
- works with no venue: A 10, B 27
- shared venues with >=2 papers in each: Electronics, IEEE Access, OSF Preprints (OSF Preprints), Preprints.org, Research Square, SSRN Electronic Journal, Zenodo (CERN European Organization for Nuclear Research), arXiv (Cornell University)

| rank | top venue A | n | top venue B | n |
|---|---|---|---|---|
| 1 | arXiv (Cornell University) | 377 | arXiv (Cornell University) | 295 |
| 2 | Zenodo (CERN European Organization for Nuclear Research) | 25 | Zenodo (CERN European Organization for Nuclear Research) | 172 |
| 3 | IEEE Robotics and Automation Letters | 19 | SSRN Electronic Journal | 29 |
| 4 | IEEE Transactions on Automatic Control | 15 | Research Square | 9 |
| 5 | IEEE Transactions on Neural Networks and Learning Systems | 12 | Electronics | 5 |
| 6 | Transactions on machine learning research | 12 | OSF Preprints (OSF Preprints) | 5 |
| 7 | IEEE Transactions on Smart Grid | 11 | PhilPapers (PhilPapers Foundation) | 5 |
| 8 | IEEE Access | 10 | IEEE Access | 5 |
| 9 | IEEE Wireless Communications Letters | 10 | Preprints.org | 4 |
| 10 | IEEE Internet of Things Journal | 10 | Applied Sciences | 4 |
| 11 | IEEE Transactions on Intelligent Transportation Systems | 9 | International Journal of Advanced Research in Science Communication and Technology | 4 |
| 12 | SSRN Electronic Journal | 9 | Applied and Computational Engineering | 3 |
| 13 | Automatica | 9 | International Research Journal of Modernization in Engineering Technology and Science | 3 |
| 14 | IEEE Transactions on Wireless Communications | 9 | INTERANTIONAL JOURNAL OF SCIENTIFIC RESEARCH IN ENGINEERING AND MANAGEMENT | 2 |
| 15 | IEEE Transactions on Mobile Computing | 9 | Figshare | 2 |

## 2d Community structure (Louvain, networkx, seed 0)

- nodes 1612 (isolated, no in-corpus edge: 614); connected nodes 998; edges 3737; cross-label edges 74 (2.0%)
- components 7, largest 978
- Louvain communities 13; purity vs A/B labels 0.923; NMI 0.424
- modularity: Louvain 0.590; A/B label partition 0.393

| community | size | A | B | top matched queries |
|---|---|---|---|---|
| 1 | 348 | 346 | 2 | safe reinforcement learning (133); constrained policy optimization (85); safe exploration (84) |
| 9 | 249 | 0 | 249 | prompt injection (141); indirect prompt injection (121); agent red teaming (8) |
| 12 | 239 | 164 | 75 | reward hacking (147); alignment faking (29); AI control (20) |
| 0 | 61 | 61 | 0 | constrained Markov decision process (27); safe reinforcement learning (20); safe exploration (11) |
| 2 | 56 | 56 | 0 | safe reinforcement learning (25); safe exploration (21); constrained Markov decision process (9) |
| 6 | 21 | 21 | 0 | constrained Markov decision process (21) |
| 8 | 5 | 5 | 0 | constrained Markov decision process (5) |
| 11 | 5 | 0 | 5 | AI control (5) |
| 5 | 4 | 4 | 0 | constrained Markov decision process (4) |
| 7 | 4 | 4 | 0 | constrained Markov decision process (3); constrained policy optimization (1) |

## 2e Time series

| year | B papers | B refs | B->A | B->B | B->A rate | B papers citing A | A papers | A refs | A->B | A->A | A->B rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2012 | 0 | 0 | 0 | 0 | n/a | 0 | 7 | 199 | 0 | 2 | 0.0% |
| 2013 | 1 | 12 | 0 | 0 | 0.0% | 0 | 7 | 152 | 0 | 0 | 0.0% |
| 2014 | 0 | 0 | 0 | 0 | n/a | 0 | 5 | 168 | 0 | 0 | 0.0% |
| 2015 | 0 | 0 | 0 | 0 | n/a | 0 | 6 | 273 | 0 | 5 | 0.0% |
| 2016 | 1 | 39 | 0 | 0 | 0.0% | 0 | 6 | 284 | 0 | 5 | 0.0% |
| 2017 | 1 | 11 | 0 | 0 | 0.0% | 0 | 11 | 402 | 1 | 19 | 0.2% |
| 2018 | 1 | 40 | 0 | 0 | 0.0% | 0 | 18 | 576 | 0 | 33 | 0.0% |
| 2019 | 3 | 79 | 0 | 0 | 0.0% | 0 | 33 | 1228 | 0 | 73 | 0.0% |
| 2020 | 3 | 200 | 0 | 0 | 0.0% | 0 | 51 | 2022 | 0 | 153 | 0.0% |
| 2021 | 6 | 95 | 0 | 1 | 0.0% | 0 | 55 | 2152 | 0 | 199 | 0.0% |
| 2022 | 10 | 282 | 0 | 0 | 0.0% | 0 | 75 | 3133 | 0 | 243 | 0.0% |
| 2023 | 16 | 645 | 0 | 6 | 0.0% | 0 | 85 | 3349 | 0 | 321 | 0.0% |
| 2024 | 49 | 1245 | 1 | 51 | 0.1% | 1 | 95 | 4173 | 0 | 429 | 0.0% |
| 2025 | 129 | 3212 | 7 | 200 | 0.2% | 5 | 140 | 6008 | 3 | 460 | 0.0% |
| 2026 | 509 | 8344 | 25 | 794 | 0.3% | 20 | 289 | 8341 | 37 | 680 | 0.4% |

## 2f Canonical works

### corpus B citing canonical works of the other culture: 15 / 729 (2.1%)

| canonical work | OpenAlex ids | citers |
|---|---|---|
| Achiam et al. 2017 Constrained Policy Optimization | https://openalex.org/W2616964725 | 1 |
| Alshiekh et al. 2018 Safe RL via Shielding | https://openalex.org/W2751422670 | 2 |
| Moldovan & Abbeel 2012 Safe Exploration in MDPs | https://openalex.org/W2151237105 | 0 |
| Ray, Achiam, Amodei 2019 Safety Gym | NOT FOUND | 0 |
| Garcia & Fernandez 2015 survey | https://openalex.org/W1845972764 | 0 |
| Amodei et al. 2016 Concrete Problems | https://openalex.org/W2462906003 | 12 |

### corpus A citing canonical works of the other culture: 24 / 883 (2.7%)

| canonical work | OpenAlex ids | citers |
|---|---|---|
| Greshake et al. 2023 indirect prompt injection | https://openalex.org/W4388886073 | 1 |
| Debenedetti et al. 2024 AgentDojo | https://openalex.org/W7128378279 | 0 |
| Greenblatt et al. 2024 Alignment Faking | https://openalex.org/W4405627013 | 19 |
| Greenblatt et al. 2023 AI Control | https://openalex.org/W4389714039 | 6 |
| Meinke et al. 2024 In-context scheming | https://openalex.org/W4405173927 | 9 |

## 3 Robustness (narrow queries)

narrow A: ['constrained policy optimization', 'shielding reinforcement learning', 'safe exploration Markov decision process']; narrow B: ['indirect prompt injection', 'alignment faking', 'jailbreak LLM agents']; sizes A 154, B 296, bridge 0

| from | total refs | within | cross | cross/total | cross/in-corpus |
|---|---|---|---|---|---|
| A -> B | 5537 | 135 | 0 | 0.0% | 0.0% |
| B -> A | 4818 | 288 | 0 | 0.0% | 0.0% |

## 3b Sensitivity (same data, no new API calls)

Cross-citations attributed to the citing paper's matched queries (a paper matching k queries counts k times):
- A -> B: [('reward hacking', 40), ('safe exploration', 1)]
- B -> A: [('alignment faking', 12), ('agentic misalignment', 10), ('AI control', 7), ('prompt injection', 2), ('LLM agent safety', 1), ('indirect prompt injection', 1)]

| variant | A | B | A->B cross/total | A->B cross/in-corpus | B->A cross/total | B->A cross/in-corpus | Louvain purity | NMI | cross-label edges |
|---|---|---|---|---|---|---|---|---|---|
| A without 'reward hacking'-only works | 689 | 729 | 1/26695 (0.0%) | 0.0% | 18/14204 (0.1%) | 1.7% | 0.993 | 0.530 | 19/3268 |
| cited >= 1 only | 703 | 351 | 33/28530 (0.1%) | 1.4% | 15/10356 (0.1%) | 1.9% | 0.938 | 0.421 | 48/3068 |

## Bridge set (matched queries of both corpora)

| year | title | queries | OpenAlex |
|---|---|---|---|
| 2025 | Natural Emergent Misalignment from Reward Hacking in Production RL | alignment faking; reward hacking | https://openalex.org/W7106695004 |
| 2026 | Drift Cascade as Thermodynamic Phase Transition in Reward Hacking: D1→D2→D3 Predicts Emergent Misalignment | alignment faking; reward hacking | https://openalex.org/W7141222905 |
| 2026 | From Reward Hacking to Coordinated Misalignment: A Systems Analysis of Loss-of-Control Risk in Frontier AI Agents | alignment faking; reward hacking | https://openalex.org/W7222945718 |
| 2026 | Inducing Emergent Misalignment from Reward Hacks with Iterative DPO | alignment faking; reward hacking | https://openalex.org/W7212077014 |
