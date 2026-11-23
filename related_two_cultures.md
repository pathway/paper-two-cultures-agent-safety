# Related work: "two cultures" framings (for "Agent Safety: The Two Cultures")

!!! warning "Status: STARTED"
    Not final. Not fully human-reviewed. See [the AI-use statement](../ai-use.md).


Date: 2026-11-20. Method: web search + page fetch + Crossref/arXiv API metadata checks. Every item in Table 1 was opened or resolved by DOI/arXiv ID.

## Answer first

- **No verified paper makes our argument.** No source found names an RL/objective-modeling culture vs an LLM-agent/behavior-modeling culture in agent safety, with or without a Breiman/Snow homage.
- **Closest partial pre-emptions:** Turner's essay that reward is not the trained agent's optimization target [31]; Çağatan & Zhao, who port RL safety gridworlds to LLM agents and find zero-shot specification gaming [29]; Dantas et al., who find specification is the bottleneck for LLM-agent safety [30]; Vernade et al., who frame RL vs control as communities with distinct "cultures" [20].
- **Existing "two cultures of AI safety" talk is a different split:** AI ethics vs AI safety (near-term vs long-term) [25][26][27][28]. [25][26][27] do not cite Snow or Breiman (full-text grep of arXiv HTML: 0 hits). Our split is orthogonal to that one.
- **Caveat:** search coverage of LessWrong/Alignment Forum posts and workshop papers is partial. Absence of evidence is not proof.

## Table 1. Verified items

Relevance: H/M/L. Pre-empts: Y/Partly/N.

| # | Citation | Content (1-2 sentences) | Two cultures named | Rel. | Pre-empts |
|---|---|---|---|---|---|
| 1 | Snow, *The Two Cultures* (1959 Rede Lecture; 2012 Canto ed.) [1] | Lecture on the communication gap between literary intellectuals and scientists. Origin of the phrase; Breiman's title alludes to it [3]. | Humanities vs natural science | M: one-line homage only | N |
| 2 | Breiman (2001), *Statistical Science* 16(3) [2] | Data-modeling culture assumes a stochastic model generated the data; algorithmic culture treats the mechanism as unknown and judges by predictive accuracy. | Data modeling vs algorithmic modeling | H: our template. Culture A = "assume the agent maximizes R" (data model); Culture B = black box judged by behavior | N |
| 3 | Norvig (2011), "On Chomsky and the Two Cultures of Statistical Learning" (essay) [3] | Replies to Chomsky's MIT 150 critique of statistical language models; explicitly invokes Breiman's two cultures. | Chomsky (explanatory model) vs statistical/probabilistic models | H: precedent for moving Breiman into AI/NLP; pre-LLM anticipation of "model the behavior, not the mind" | N |
| 4 | Shmueli (2010), "To Explain or to Predict?", *Stat. Sci.* 25(3) [4] | Explanatory and predictive modeling differ in goals, data, validation; conflating them causes errors. | Explanatory vs predictive modeling | M: "explain the objective" vs "predict the behavior" | N |
| 5 | Donoho (2017), "50 Years of Data Science", *JCGS* 26(4) [5] | Has a section on Breiman's two cultures; names the Common Task Framework (shared data, shared metric, leaderboard) as the predictive culture's "secret sauce". | Generative/inferential vs predictive culture | H: CTF = evals/benchmarks as the operational specification of Culture B | N |
| 6 | Efron (2020), "Prediction, Estimation, and Attribution", *JASA* 115(530) [6] | Updates Breiman: pure prediction algorithms neglect estimation and attribution; hopes for reunification. | Prediction vs estimation/attribution | M: attribution ~ "why did the agent act" | N |
| 7 | *Observational Studies* 7(1) (2021), special issue reprinting Breiman with ~30 comments; Introduction by Mitra [7] | Twenty-year retrospective. Shows that "two cultures" papers are expected to end in synthesis. | Same as [2] | M: cite once as the canonical follow-up venue | N |
| 8 | Ogburn & Shpitser (2021), "Causal Modelling: The Two Cultures", *Obs. Stud.* 7(1):179-183 [8] | Applies the two-cultures frame to causal modeling (title and venue verified; full text behind access wall, content not read). | Causal-modeling cultures (not read) | M: direct precedent for re-deploying the title in a new field | N |
| 9 | Pearl (2021), "Causally Colored Reflections on Breiman's Two Cultures", *Obs. Stud.* 7(1):187-190; blog version 2020 [9] | Argues Breiman's two cultures are both descriptive (interpretable vs uninterpretable); neither is causal. | Interpretable vs uninterpretable description; causal as missing third | H: analog for our claim that black-box evals predict behavior but do not license intervention/guarantee claims | N |
| 10 | D'Amour (2021), "Revisiting Rashomon", *Obs. Stud.* 7(1):59-63; arXiv:2104.02150 [10] | Many models fit equally well but process data differently (Rashomon effect); links to underspecification. | Same as [2] | H: many policies pass the same eval suite but differ off-distribution. Core of "evals underdetermine the agent" | N |
| 11 | Miller, Foti & Fox (2021), "Breiman's two cultures: You don't have to choose sides", *Obs. Stud.* 7(1):161-169; arXiv:2104.12219 [11] | Adds mechanistic models as a third point; hybrids interpolate. | Data vs algorithmic, + mechanistic | M: template for a synthesis section (e.g., shields around black-box LLM agents) | N |
| 12 | Mentch & Hooker (2021), "Bridging Breiman's Brook", *Obs. Stud.* 7(1):107-125; arXiv:2102.12328 [12] | Twenty years on the divide is "ephemeral"; data modelers absorbed algorithmic methods. | Same as [2] | M: counter-argument we must address ("the split will dissolve") | N |
| 13 | Kass (2021), "The Two Cultures: Statistics and Machine Learning in Science", *Obs. Stud.* 7(1):135-144 [13] | Statistician's view of the stats-ML divide in scientific use. | Statistics vs ML | L | N |
| 14 | Other *Obs. Stud.* 7(1) comments with "culture(s)" in title [14]: Bühlmann "One Modern Culture of Statistics"; Neufeld & Witten "From Two Cultures to One"; Shmueli "From Two Cultures to Multicultural"; Imbens & Athey "A Perspective from Econometrics"; Freeman et al. "Beyond Two Cultures: Cultural Infrastructure for Data-driven Decision Support"; Bonvini, Mishler & Kennedy (causal), arXiv:2103.15281 | Titles/DOIs verified via Crossref; Bonvini et al. abstract read (model complexity vs causal misinterpretation). | Same as [2] | L-M: Freeman et al. (decision support) is nearest to agents | N |
| 15 | Raper (2020), "Leo Breiman's 'Two Cultures'", *Significance* 17(1):34-37 [15] | Short retrospective for a general statistics audience. | Same as [2] | L | N |
| 16 | Mukhopadhyay & Wang (2020), "Breiman's 'Two Cultures' Revisited and Reconciled", arXiv:2005.13596 [16] | Proposes an integrated statistical-learning framework to blend the cultures. | Parametric statistical vs algorithmic ML | L | N |
| 17 | Rudin (2025), "Leo Breiman, the Rashomon Effect, and the Occam Dilemma", arXiv:2507.03884 [17] | Argues the Rashomon set lets accurate models also be simple; separates interpretability from causality. | Data vs algorithmic | M: supports "Rashomon set of safe-looking agents" argument | N |
| 18 | Su (2025, v3 2026), "Do Large Language Models (Really) Need Statistical Foundations?", arXiv:2505.19145 [18] | Argues LLMs need statistics because they are black boxes; maps Breiman's data-modeling culture to Efron's estimation/attribution. | Breiman/Efron cultures applied to LLMs | M: shows Breiman already used to frame LLM research; not safety, not agents | N |
| 19 | Recht (2019), "A Tour of Reinforcement Learning: The View from Continuous Control", *Annu. Rev. Control Robot. Auton. Syst.* 2:253-279; arXiv:1806.09460 [19] | Surveys RL from the optimization/control side; compares model-free and model-based methods on LQR. | RL vs control (implicit; not called "cultures") | H: anchor for the RL-vs-control mapping (Culture A inherits control's model-based guarantees) | N |
| 20 | Vernade, Eberhard, White, Dörfler, Szepesvári, Krstic, Muehlebach (2026), "Foundations of RL and Control: Connections and New Perspectives", INFORMS TutORials 187-212; arXiv:2608.02433 [20] | States RL and control share DP roots but "evolved with distinct methodologies, goals, and cultures"; a gap persists between the communities. No Breiman/Snow citation (grep: 0 hits). | RL vs control | H: most recent authoritative statement of the RL/control split | Partly (for the RL-vs-control sub-argument only) |
| 21 | Gowers (2000), "The Two Cultures of Mathematics", in *Mathematics: Frontiers and Perspectives*, AMS [21] | Explicit Snow homage; problem-solvers vs theory-builders; both needed; one is undervalued. | Problem-solvers vs theory-builders | L-M: optional analogy (Culture B "solves cases"; Culture A "builds theory") | N |
| 22 | Carrington & Stocks (1994), "A tale of two paradigms: Formal methods and software testing", Z User Workshop [22] | Two camps: formal-methods advocates vs testing traditionalists; argues for combining. | Formal methods vs testing | H: direct software-engineering precedent of our split (shields/CMDP proofs vs evals/red-teaming) | N |
| 23 | Blackwell (2025), "Two cultures of interdisciplinarity", *Cambridge Forum on AI: Culture and Society* 1:e1 [23] | Re-reads Snow and Agre for AI; contrasts descriptive specification (symbolic) vs reactive imitation (statistical ML). | Making vs critique; specification vs imitation | M: "specification vs imitation" is close to objective vs behavior | N |
| 24 | Koch & Peterson (2024), "From Protoscience to Epistemic Monoculture: How Benchmarking Set the Stage for the Deep Learning Revolution", arXiv:2404.06647 [24] | Sociological history: benchmarking produced an AI "epistemic monoculture"; cites Breiman's two cultures. | Explanation vs prediction (via Breiman) | M: critique of Culture B's reliance on benchmarks | N |
| 25 | Bristow, Thorburn & Acosta-Navas (2023), "Views on AI aren't binary -- they're plural", arXiv:2312.14230 [25] | Argues the "AI Ethics" vs "AI Safety" binary is false and harmful. | AI ethics vs AI safety | M: shows a different safety binary exists; also warns against binaries | N |
| 26 | Roytburg & Miller (2025), "Mind the Gap! Pathways Towards Unifying AI Safety and Ethics Research", arXiv:2512.10058 [26] | Bibliometric study of 6,442 papers: >80% of collaborations stay within safety or ethics. | AI safety vs AI ethics | M: quantitative method we could copy (co-authorship split RL-safety vs LLM-safety) | N |
| 27 | Gyevnár & Kasirzadeh (2026), "Bridging the Gap in the Responsible AI Divides", arXiv:2603.14495 [27] | Four modes of engagement between AIS and AIE; computational analysis of 3,555 papers. | AI safety vs AI ethics | M: same as [26] | N |
| 28 | Ahmed, Jaźwińska, Ahlawat, Winecoff (2024), "Field-building and the epistemic culture of AI safety", *First Monday* [28] | Ethnography of the AI-safety community's epistemic culture (forums, forecasting, prizes). | (single culture studied) | L | N |
| 29 | Çağatan & Zhao (2026), "Reward Hacking in Language Model Agents: Revisiting AI Safety Gridworlds", arXiv:2606.15385 [29] | Ports RL safety gridworlds to text for LLM agents; specification gaming appears zero-shot; RL fine-tuning widens observed-vs-hidden reward gap. | None named (empirical bridge) | H: direct evidence that Culture A's problems reappear in Culture B's agents | Partly |
| 30 | Dantas, Cordeiro, Nowroozi, Tihanyi (2026), "Toward Safe LLM Agents: A Survey of Specification, Verification, and Enforcement", arXiv:2608.14590 [30] | PRISMA review of 38 studies; specification is the bottleneck; runtime monitoring most mature. No safe-RL/CMDP coverage (grep: 0 hits). | None named | H: supports "evals-as-specification"; shows formal methods entering Culture B without safe-RL | Partly |
| 31 | Turner (2022), "Reward is not the optimization target", Alignment Forum essay [31] | Argues RL-trained policies need not optimize reward; reward shapes cognition. | None named | H: undercuts Culture A's core assumption for trained agents | Partly |

## Not verified / not found

- **"The two cultures of AI safety"** as an exact title or framing: not found.
- **Any paper that frames RL community vs LLM community as two cultures:** not found (extended searches).
- **Bertsekas "two cultures" of RL/control:** no source found that uses the term.
- **Ogburn & Shpitser [8]:** title, pages, DOI verified; content not read (Project MUSE access wall).
- **Kass [13]:** DOI verified; author PDF did not parse.
- **Gowers [21]:** PDF and book title confirmed by search listing; page numbers not verified; PDF fetch failed (TLS error).
- **Su [18]:** fetch summary said venue is *Annals of Applied Statistics*; not confirmed on a publisher page.

## Most relevant works

1. **Breiman 2001 [2]** - Intro homage and structure. Map: data model -> "assume agent maximizes R"; algorithmic model -> "black box, judged by behavior".
2. **Donoho 2017 [5]** - Evals-as-specification. The Common Task Framework is how Culture B defines "correct"; agent evals/red-teaming are its safety analog.
3. **D'Amour 2021 [10]** (+ Rudin 2025 [17]) - Evals-as-specification limit. Rashomon/underspecification: an eval suite does not pin down the agent.
4. **Recht 2019 [19] + Vernade et al. 2026 [20]** - RL-vs-control mapping. Vernade et al. is the one place "cultures" is used for RL vs control.
5. **Carrington & Stocks 1994 [22]** - Related work. Formal methods vs testing is the software-engineering ancestor of shields/CMDPs vs evals.
6. **Pearl 2021 [9]** (+ Ogburn & Shpitser 2021 [8]) - Related work / synthesis. Both Breiman cultures are descriptive; neither alone gives intervention guarantees. Parallel: neither assumed-R nor eval scores alone give safety guarantees.
7. **Norvig 2011 [3]** - Intro. Precedent for carrying Breiman into AI.
8. **Bristow et al. 2023 [25] / Roytburg & Miller 2025 [26]** - Related work. State that our split is not the ethics-vs-safety split.
   - Pre-emption paragraph: Turner 2022 [31], Çağatan & Zhao 2026 [29], Dantas et al. 2026 [30].
   - Snow [1]: one sentence in the intro.

## Bibliography

[1] C. P. Snow, *The Two Cultures* (Rede Lecture, 1959), with introduction by S. Collini. Cambridge: Cambridge University Press, Canto Classics, 2012. https://doi.org/10.1017/CBO9781139196949

[2] L. Breiman, "Statistical Modeling: The Two Cultures (with comments and a rejoinder by the author)," *Statistical Science*, vol. 16, no. 3, pp. 199-231, 2001. https://doi.org/10.1214/ss/1009213726

[3] P. Norvig, "On Chomsky and the Two Cultures of Statistical Learning," essay, 2011. https://www.norvig.com/chomsky.html

[4] G. Shmueli, "To Explain or to Predict?," *Statistical Science*, vol. 25, no. 3, pp. 289-310, 2010. https://doi.org/10.1214/10-STS330

[5] D. Donoho, "50 Years of Data Science," *Journal of Computational and Graphical Statistics*, vol. 26, no. 4, pp. 745-766, 2017. https://doi.org/10.1080/10618600.2017.1384734

[6] B. Efron, "Prediction, Estimation, and Attribution," *Journal of the American Statistical Association*, vol. 115, no. 530, pp. 636-655, 2020. https://doi.org/10.1080/01621459.2020.1762613

[7] N. Mitra, "Introduction," *Observational Studies*, vol. 7, no. 1, pp. 1-2, 2021 (special issue on Breiman's "Two Cultures"). https://doi.org/10.1353/obs.2021.0015

[8] E. L. Ogburn and I. Shpitser, "Causal Modelling: The Two Cultures," *Observational Studies*, vol. 7, no. 1, pp. 179-183, 2021. https://doi.org/10.1353/obs.2021.0006

[9] J. Pearl, "Causally Colored Reflections on Leo Breiman's 'Statistical Modeling: The Two Cultures' (2001)," *Observational Studies*, vol. 7, no. 1, pp. 187-190, 2021. https://doi.org/10.1353/obs.2021.0008 ; blog version: https://causality.cs.ucla.edu/blog/index.php/2020/10/14/causally-colored-reflections-on-leo-breimans-statistical-modeling-the-two-cultures-2001-https-projecteuclid-org-download-pdf_1-euclid-ss-1009213726/

[10] A. D'Amour, "Revisiting Rashomon: A Comment on 'The Two Cultures'," *Observational Studies*, vol. 7, no. 1, pp. 59-63, 2021. https://doi.org/10.1353/obs.2021.0022 ; https://arxiv.org/abs/2104.02150

[11] A. C. Miller, N. J. Foti, and E. B. Fox, "Breiman's Two Cultures: You Don't Have to Choose Sides," *Observational Studies*, vol. 7, no. 1, pp. 161-169, 2021. https://doi.org/10.1353/obs.2021.0003 ; https://arxiv.org/abs/2104.12219

[12] L. Mentch and G. Hooker, "Bridging Breiman's Brook: From Algorithmic Modeling to Statistical Learning," *Observational Studies*, vol. 7, no. 1, pp. 107-125, 2021. https://doi.org/10.1353/obs.2021.0027 ; https://arxiv.org/abs/2102.12328

[13] R. E. Kass, "The Two Cultures: Statistics and Machine Learning in Science," *Observational Studies*, vol. 7, no. 1, pp. 135-144, 2021. https://doi.org/10.1353/obs.2021.0000

[14] P. Bühlmann, "One Modern Culture of Statistics," https://doi.org/10.1353/obs.2021.0020 ; J. Neufeld and D. Witten, "From Two Cultures to One," https://doi.org/10.1353/obs.2021.0004 ; G. Shmueli, "From Two Cultures to Multicultural," https://doi.org/10.1353/obs.2021.0010 ; G. Imbens and S. Athey, "Breiman's Two Cultures: A Perspective from Econometrics," https://doi.org/10.1353/obs.2021.0028 ; A. Freeman et al., "Beyond Two Cultures: Cultural Infrastructure for Data-driven Decision Support," https://doi.org/10.1353/obs.2021.0024 ; M. Bonvini, A. Mishler, E. H. Kennedy, "Comment on 'Statistical Modeling: The Two Cultures'," https://doi.org/10.1353/obs.2021.0001 , https://arxiv.org/abs/2103.15281 . All in *Observational Studies*, vol. 7, no. 1, 2021.

[15] B. Raper, "Leo Breiman's 'Two Cultures'," *Significance*, vol. 17, no. 1, pp. 34-37, 2020. https://doi.org/10.1111/j.1740-9713.2020.01357.x

[16] S. Mukhopadhyay and K. Wang, "Breiman's 'Two Cultures' Revisited and Reconciled," arXiv:2005.13596, 2020. https://arxiv.org/abs/2005.13596

[17] C. Rudin, "Leo Breiman, the Rashomon Effect, and the Occam Dilemma," arXiv:2507.03884, 2025. https://arxiv.org/abs/2507.03884

[18] W. Su, "Do Large Language Models (Really) Need Statistical Foundations?," arXiv:2505.19145, 2025 (v3 2026). https://arxiv.org/abs/2505.19145

[19] B. Recht, "A Tour of Reinforcement Learning: The View from Continuous Control," *Annual Review of Control, Robotics, and Autonomous Systems*, vol. 2, pp. 253-279, 2019. https://doi.org/10.1146/annurev-control-053018-023825 ; https://arxiv.org/abs/1806.09460

[20] C. Vernade, O. Eberhard, M. White, F. Dörfler, Cs. Szepesvári, M. Krstic, and M. Muehlebach, "Foundations of Reinforcement Learning and Control: Connections and New Perspectives," in *INFORMS TutORials in Operations Research*, pp. 187-212, 2026. https://doi.org/10.1287/educ.2026.0310 ; https://arxiv.org/abs/2608.02433

[21] W. T. Gowers, "The Two Cultures of Mathematics," in V. Arnold et al. (eds.), *Mathematics: Frontiers and Perspectives*, American Mathematical Society, 2000. https://www.dpmms.cam.ac.uk/~wtg10/2cultures.pdf

[22] D. Carrington and P. Stocks, "A tale of two paradigms: Formal methods and software testing," in *Z User Workshop, Cambridge 1994*, Workshops in Computing, Springer, pp. 51-68, 1994. https://doi.org/10.1007/978-1-4471-3452-7_4

[23] A. F. Blackwell, "Two cultures of interdisciplinarity," *Cambridge Forum on AI: Culture and Society*, vol. 1, e1, 2025. https://doi.org/10.1017/cfc.2025.10003

[24] B. J. Koch and D. Peterson, "From Protoscience to Epistemic Monoculture: How Benchmarking Set the Stage for the Deep Learning Revolution," arXiv:2404.06647, 2024. https://arxiv.org/abs/2404.06647

[25] T. Bristow, L. Thorburn, and D. Acosta-Navas, "Views on AI aren't binary -- they're plural," arXiv:2312.14230, 2023. https://arxiv.org/abs/2312.14230

[26] D. Roytburg and B. Miller, "Mind the Gap! Pathways Towards Unifying AI Safety and Ethics Research," arXiv:2512.10058, 2025. https://arxiv.org/abs/2512.10058

[27] B. Gyevnár and A. Kasirzadeh, "Bridging the Gap in the Responsible AI Divides," arXiv:2603.14495, 2026. https://arxiv.org/abs/2603.14495

[28] S. Ahmed, K. Jaźwińska, A. Ahlawat, and A. Winecoff, "Field-building and the epistemic culture of AI safety," *First Monday*, vol. 29, no. 4, 2024. https://doi.org/10.5210/fm.v29i4.13626

[29] Ö. V. Çağatan and X. Zhao, "Reward Hacking in Language Model Agents: Revisiting AI Safety Gridworlds," arXiv:2606.15385, 2026. https://arxiv.org/abs/2606.15385

[30] P. Dantas, L. Cordeiro, E. Nowroozi, and N. Tihanyi, "Toward Safe LLM Agents: A Survey of Specification, Verification, and Enforcement," arXiv:2608.14590, 2026. https://arxiv.org/abs/2608.14590

[31] A. M. Turner, "Reward is not the optimization target," Alignment Forum, 2022. https://www.alignmentforum.org/posts/pdaGN6pQyQarFHXF4/reward-is-not-the-optimization-target
