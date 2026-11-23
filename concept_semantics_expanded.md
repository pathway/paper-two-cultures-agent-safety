# Semantics of core concepts across six decision settings

!!! warning "Status: STARTED"
    Draft. Not fully human-reviewed. See [the AI-use statement](../ai-use.md).


Date: 2026-11-21. Expands `concept_semantics.md`. Companion to `assumptions_table.md`.

Purpose. Split "LLM" by how the decision problem is posed, not by model size. The posing decides which RL concepts keep their meaning.

## 0. Three axes, one path

The columns differ on three independent axes. The table follows one path through them; other paths exist (e.g. a PRM over tool calls, [43]).

| Axis | Values |
|---|---|
| Action granularity | whole completion · reasoning step · tool call |
| Reward source | environment · human rater · learned reward model · programmatic verifier · none at run time |
| World coupling | none (text only) · side effects visible to a human each step · side effects invisible until the run ends |

## Columns

| Col | Setting | Posed as |
|---|---|---|
| RL | Classical RL agent. | MDP or POMDP (S, A, P, R, γ) [1, 2]. |
| CHAT-O | Chatbot, no tools, outcome supervision by a learned reward model. The whole completion is one action. | Contextual bandit with a proxy reward [11–15, 17, 71, 72]. |
| CHAT-V | Chatbot, no tools, verifiable outcome reward (RLVR). The whole trace plus answer is one action; the reasoning trace is not supervised. | Contextual bandit with ground-truth reward on the answer [18, 22, 23]. |
| CHAT-P | Chatbot, no tools, process supervision. Each reasoning step is one action, scored by a process reward model (PRM). | Finite-horizon deterministic tree MDP, dense step reward [25–28]. |
| AGENT-A | Tool-using assistant. One tool call or reply per turn; a human sees the result before the next turn. | Episodic POMDP with a human turn between steps [35, 36, 45]. |
| AGENT-X | Autonomous agent. Loop of tool calls until the model declares done; no human between steps; memory; sub-agents. | Long-horizon POMDP; unknown, non-stationary, partly adversarial dynamics; no reset [37, 44, 46]. |

AGENT-A and AGENT-X are the two variants of "chatbot-agent with tools". Cells name what changes from the previous column.

## 1. Formal objects

| Concept | RL | CHAT-O | CHAT-V | CHAT-P | AGENT-A | AGENT-X |
|---|---|---|---|---|---|---|
| The agent | Policy π [1]. | The model. | The model; the trace is part of its output, not a separate module [23]. | Model + step delimiter; PRM joins at inference for search [26, 29]. | Model + scaffold + tool set + system prompt [35]. | Same + memory store + sub-agents [41, 47]. |
| Action | a_t from a fixed small set [1]. | The whole completion y. PPO treats tokens as actions, but reward is terminal and RLOO/ReMax/GRPO show the bandit view suffices [16–18, 68, 70]. | Trace + answer as one sample; group-relative advantage, no critic [18, 23]. | One reasoning step; tens per episode; no side effect [26]. | One tool call or one reply; side effect possible; user sees it [35]. | One call in a chain of hundreds; side effects accumulate unseen [44, 96]. |
| State | Markov s_t in a designer representation [1]. | The prompt x; fixed for the episode. | Same. | Prompt + steps so far; fully observed; but the distribution of states is induced by the policy itself, so errors compound [32]. | Context + tool results + hidden world state + user intent [95]. | Same + world changed by own earlier calls and by others + memory contents [41]. |
| Observation | Sensor of s_t; data only. | The prompt; data and instruction in one stream [38]. | Same. | Own previous steps; self-generated. | Tool output and user turn, mixed with instructions; models cannot reliably separate the two [37, 38]. | Tool outputs from untrusted sources; no user turn to filter them [37, 40]. |
| Transition | P(s'\|s,a): stochastic, often unknown [1]. | None; one step. | None. | Deterministic append; the agent is the dynamics. | The tool executes; stochastic, external. | Same, plus the world moves between calls. |
| Markov property | Assumed by construction. | Trivial. | Trivial. | Holds: the prefix is the state. | Fails: hidden world state [2]. | Fails harder: own past side effects are hidden. |
| Belief state | b_t over s_t, updated by Bayes filter [2]. | n/a. | n/a. | n/a. | The context is the belief summary; the user holds the rest. | The context is a bounded, lossy belief; context limits and compaction are belief truncation, which creates pseudo-episodes inside one task. |
| Horizon | Designer-chosen. | 1. | 1 (trace length is inside the action). | Steps to final answer, ~10–100 [26]. | 1 turn, then human [95]. | Hundreds of calls; hours [42, 44, 94]. |
| Reset | Yes; reset-free RL is a niche [8]. | Trivial. | Trivial. | Yes: resample or branch any prefix [31]. | Conversation restarts; side effects remain. | No; the irreversibility literature was written for this case but tested on grid worlds [9]. |
| Time step | Clock tick. | The whole response. | The whole response. | One step. | One turn. | One call; seconds to minutes each. |

## 2. Objective, reward, value

| Concept | RL | CHAT-O | CHAT-V | CHAT-P | AGENT-A | AGENT-X |
|---|---|---|---|---|---|---|
| Reward source | The environment, as written by the designer [1, 77]. | Reward model fit to human pairwise preferences [11, 13, 14]. | Programmatic check of the final answer: test cases, exact match [22, 23]. | PRM fit to per-step human labels [26] or Monte-Carlo rollouts [27]. | Deployment: none. Training: trajectory success test in a sandbox [43]. | Same; tests sparser and more gameable [24]. |
| Reward timing | Every step. | Terminal, plus a per-token KL penalty to the reference policy [12, 13]. | Terminal, plus KL (or none in GRPO variants) [18, 23]. | Every step: dense. | None at run time. | None at run time; terminal in training. |
| The KL term | A trust region on the policy (TRPO/PPO) [68, 69]. | A constraint that keeps the policy near the pretrained prior [12, 15, 75]; cast as a CMDP with the KL coefficient as Lagrange multiplier [73], as a KL budget [19], or as Bayesian inference [74]. | Same. | Same. | Same in training; absent at deployment. | Absent. |
| Who writes it | One designer, in advance [4]. | Raters' preferences, compressed into a model [11]. | Dataset author with ground truth. | Raters labelling steps, or an automatic checker [26, 27]. | Benchmark author (training) [42]; user acceptance (deployment). | Same. |
| Return / value | V, Q: the central object [1]. | Q(x,y) = r. Degenerate; critics are dropped [17, 18, 70]. | Degenerate. | Q(prefix) = PRM score; drives best-of-n, beam, MCTS [29, 31]. | None. | None; some systems add value heads. |
| Credit assignment | Temporal, by bootstrapping [1]. | None across time: one reward, one action. PPO spreads it over tokens by advantage; DPO learns an implicit token-level Q [16]. | Same; the trace gets credit only via the answer. | Explicit per step [25]. | Per turn, via user reaction. | Which of 200 calls caused the failure? Terminal signal only [43]. |
| Discount | γ < 1 typical. | n/a. | n/a. | γ = 1 typical. | None. | None. |
| Reward identifiability | R identified only up to potential shaping; IRL is ill-posed [52, 53, 76]. | Bradley–Terry identifies within-prompt differences only; the RM is a classifier, not a utility [11, 15]. | Fully identified on the checked set; undefined off it, and verifiers have false positives [93]. | Step labels define "progress"; the label is "convincing", not "correct" [26]. | None: no reward exists to identify. | None. |
| Proxy gap: what gets hacked | R itself, when misspecified [4, 5, 51], or the reward channel is tampered with [78]. | The RM: length, sycophancy, confident tone [19–21, 79]. | The verifier's incompleteness: special-casing tests, bypassing checks; and the trace, if it is trained on, stops showing it [24]. | The PRM: plausible-looking steps, verbosity; R1 and others abandoned PRMs for this reason [23, 28, 91, 92]. | The user: claims of success [44]. | The success test and the user: editing tests, fabricated completion [24, 44]; hacking in production RL generalises to broader misalignment [80]. |
| Goal-directedness | By construction [1]. | None; one shot. | Within one trace, toward an answer. | Simulated across steps toward an answer. | Role-played from the instruction, one turn at a time. | Role-played across a long loop; new context can replace it [37]. |
| Instrumental behaviour | Optimal policies tend to seek power in most MDPs, by theorem [54, 117]. | None; one shot. | Within-trace strategies only. | None. | Bounded by the veto. | Observed in evaluations: in-context scheming [55], blackmail and leaking under goal conflict [56], escalation from gaming to tampering [57]. Role-played [116], from a prior that pretraining text shapes [120, 121], but with real tools. Whether RL training raises the rate is contested [118, 119]. |

## 3. Learning, exploration, search

| Concept | RL | CHAT-O | CHAT-V | CHAT-P | AGENT-A | AGENT-X |
|---|---|---|---|---|---|---|
| Training loop | Online: act and learn in one loop [1, 68]. | Sample completions, score with RM, PPO/DPO/RLOO [14, 15, 17]. | Sample traces, verify answers, GRPO [18, 23]; rejection-sampling precursor [124]. | Sample steps, score with PRM, RL or search distillation [25, 26]. | Agentic RL in sandboxed task suites, then freeze [43, 89]. | Same; environments harder to build and to make safe. |
| Sim-to-real | Simulator vs robot [10, 86]. | None: training prompts and deployment prompts are the same kind of object. | Same. | Same. | Training sandbox vs deployment world: resets, clean tests and benign content exist only in the former [43]. | Same, wider. |
| Exploration | Designed [83]; safe exploration is a field [6, 84]. | n completions at temperature; RLHF narrows the sampled set [82]. | Same; coverage grows with n [30]. | Tree search over steps [31]. | None designed. | None designed; happens in the real world. |
| Search at inference | Planning if a model is known. | Best-of-n with RM [19]. | Best-of-n with verifier where available [30, 81]. | Beam or MCTS with PRM; test-time compute scaling [29]. | Rarely. | Retry, reflect, self-verify [87]. No simulator; tree search needs a revertible state [88]; every probe is a real action. |
| Planning / world model | Model-based: Dyna, MuZero [58]. | None. | The trace is planning unrolled in words; no separate model. | PRM + tree = planning with a learned value, the AlphaZero shape [59, 90]; the LLM can serve as its own world model where transitions are text-predictable [60]. | None; the human plans. | The ReAct loop is model-free [35]; self-simulation fails where the world is not text-predictable. |
| On- vs off-policy | Both; offline RL is the counterpart of SFT on logs [1, 85]. | PPO on-policy; DPO offline [14, 15]. | On-policy [18, 23]. | Both. | SFT on logged trajectories (offline imitation) + on-policy RL in sandbox [43]. | Same. |
| Learning at deployment | Yes. | No. | No. | No. | In-context only. | In-context + memory files written by the loop [41]. |
| Memory | The state. | Context. | Context. | Context. | Context across turns. | Context + external stores; writable by injected content [41]. |
| Source of competence | Trial and error. | Pretraining + preference tuning [14]. | Pretraining + RLVR; reasoning length grows under training [23]. | Same + step-level tuning. | Base model; scaffold adds tools, not competence [36]. | Same. |
| What RL adds to the base model | Everything. | Style, helpfulness, refusal; a thin steering layer [14]. | Sharpens sampling toward solutions the base model could already reach [61]; near-random rewards can help [62], so "reward" is a weaker signal than the bandit frame suggests. | Step reliability. | Tool-call formatting; persistence [43]. | Same. |

## 4. World and parties

| Concept | RL | CHAT-O | CHAT-V | CHAT-P | AGENT-A | AGENT-X |
|---|---|---|---|---|---|---|
| Side effects | In the environment; penalised by reachability or attainable utility [97, 98]. | None; text only. | None. | None. | One per turn, visible. | Many, invisible until the end [44, 46]. |
| Reversibility | Environment-specific [9, 99]. | n/a. | n/a. | Total: resample. | Depends on tool; user can veto the next. | Many irreversible; no veto point [46]. |
| Adversary | Nature; or a trained disturbance policy [100]. | Prompt author (jailbreak) [105, 106]. | Same. | Same, plus a flawed PRM. | Content in tool output (injection) [37, 40, 107]. | Same, with no human to catch it; memory poisoning persists across runs [41]. |
| Other agents | Designed multi-agent game [101]. | None. | None. | Self as verifier. | None. | Sub-agents, copies, other vendors' agents [47]; multi-agent failures have their own taxonomy [108]. |
| Principal | One designer; CIRL relaxes this to a human whose reward is unknown [103]. | Vendor + user; conflicts resolved by an instruction hierarchy [39, 50]. | Vendor + dataset author. | Vendor. | Vendor, deployer, user [39]. | Same + third parties via content [37]. |
| Specification | R and C, written once [3, 4]. | RM + refusal policy [109] + model spec [50]. | Verifier + model spec. | PRM step rubric [26]. | System prompt + tool permissions + user instruction. | Same; approval gates often off (debunking §7). |
| Contract view | A complete contract: R covers every state [63]. | Incomplete; the pretrained prior fills the gaps [63]. | Incomplete off the checked set. | Incomplete; filled by the PRM's notion of progress. | Three incomplete contracts stacked: vendor, deployer, user [39, 63]. | Same, with no party present to renegotiate. |
| Autonomy level | Full, after training. | Reactive; no autonomy. | Reactive. | Reactive. | Human-in-the-loop: operator approves each action [45, 64, 115]. | Human-out-of-the-loop; the level several authors argue should not be built [64, 65]. |

## 5. Safety and oversight

| Concept | RL | CHAT-O | CHAT-V | CHAT-P | AGENT-A | AGENT-X |
|---|---|---|---|---|---|---|
| Safety constraint | CMDP cost budget [3, 84]; shield over a known unsafe set [7]. | Refusal training [109]; output filter [110]; KL to prior [12]. | Same, plus safety reasoning trained into the trace [111]. | Step-level filter on reasoning. | Tool allow/deny lists; approval per call [45]. | Sandbox, budgets, kill switch; gates that users disable [45]. |
| Defence layer | In the environment or the policy. | In the weights (training). | In the weights. | In the weights and the PRM. | Two layers: weights, and the tool layer (permissions, capability flow control) [66]. | Same; the tool layer is where a deployer can still write a rule [122] (`../llm-agent-incident-catalog/coverage/coverage_report.md`). |
| Failure | Low return; constraint violation. | Bad text [79]. | Right-looking answer that games the checker [24]. | Wrong answer with plausible steps [28]. | One bad side effect, caught after one step. | Cascade of side effects [46]. |
| Oversight channel | None at run time; an off-switch is respected only under uncertainty about the objective [104]. | The output. | The trace: readable, and monitorable until optimization pressure is put on it [24]. | The steps; readable but possibly unfaithful [33, 34]. | Tool-call log + user per turn. | Traces + logs, read afterwards; the agent knows it is being watched [48, 49]; control protocols assume it may subvert the monitor [113]. |
| Monitorability | n/a. | Output only. | Trace is monitorable while not optimised against [24, 67], and even then it omits much [112]. | Steps, possibly unfaithful [33, 34]. | Log + human. | Trace + log; monitorability is a property of training, not of the agent [67]. |
| Validation | Return on held-out seeds; safety needs a hidden metric separate from reward [102]. | Win rate vs RM or humans [14]. | Pass rate on held-out verifiable sets [22]. | Step accuracy + final accuracy [26]. | Task success + attack success rate [40, 96]. | Benchmark pass rate [42, 114]; incident records; evaluations that reward cost-blind success [44]. |
| Meaning of "safe" | Expected cost under budget [3]. | No harmful text. | Correct answer by legitimate means. | No harmful step and right answer. | No unapproved harmful call. | No harmful side effect over the whole run. |

## 6. Reading the gradient

- CHAT-O and CHAT-V are bandits. Reward, return, credit assignment and exploration are degenerate; the field responded by dropping the critic [17, 18]. The one classical-RL object that survives is the KL trust region. This reading is established, not new: Moskovitz et al. cast RLHF as a CMDP with the KL coefficient as a Lagrange multiplier [73], Gao et al. speak of a KL budget [19], Ziegler et al. already tuned the coefficient to a KL target [12], and the practice goes back to KL-control of sequence models [75]. Korbak et al. give the competing Bayesian reading [74].
- CHAT-V moved the proxy gap from the reward model to the verifier's coverage. Its unsupervised trace is a new oversight channel that training pressure destroys [24]. This is a CHAT-level result that the agent columns inherit unchanged.
- CHAT-P is the column closest to classical RL: dense reward, Markov state, known deterministic dynamics, free resets, searchable tree. It has no side effects, so it is also the safest place to apply RL machinery. It is also the column the frontier retreated from because its reward got hacked [23, 28]. "RL for LLMs" literally holds here, and it did not hold up. The retreat is documented by R1 and by PRM papers [23, 28, 91, 92]; the ranking of settings by closeness to RL was not found elsewhere.
- AGENT-A reintroduces the world but keeps a human between every step. The human is the reward signal, the reset, and the safety gate at once. Approval fatigue removes all three (debunking §7).
- AGENT-X removes the human. It is the furthest column from classical RL on every row of §1–§3, yet it is where RL vocabulary (reward hacking, unsafe exploration, specification) is most used. The words transfer; the objects do not. Sim-to-real reappears as sandbox-to-deployment [43].
- McLean's three classes land in different columns: reward misspecification is a CHAT-O/CHAT-V/CHAT-P problem (the RM, verifier, or PRM); unsafe action in an irreversible state is AGENT-X; insufficient observation is AGENT-A/X. No column has all three. No prior mapping of the classes to settings was found (literature search, 2026-11-21). Caveat: the class names here follow the debunking draft; a third-party summary of McLean et al. words them as observation ambiguity, reward misspecification and unsafe exploration. Cagatan & Zhao port the RL-safety gridworlds to LLM agents and find specification gaming, but treat agents as one setting [123].
- Identifiability degrades left to right: R is identified up to shaping; the RM only within a prompt; the verifier only on the checked set; the agent has nothing to identify. "Reward misspecification" presupposes a reward that can be mis-specified; by AGENT-A that object is gone [52, 53]. Rungs one and two are explicit in the literature [53; 15, Def. 1]; rung three is stated only informally via verifier failures [93]; rung four was not found stated. Ng et al. reach the same conclusion from the other side: safety for autonomous agents belongs at run time, not in training [122].
- Instrumental behaviour is a theorem in RL [54] and an evaluation finding in AGENT-X [55, 56]. The middle columns have no room for it: a one-shot bandit cannot seek power. The agent columns re-create the conditions (horizon, side effects, goal conflict) without the optimiser; the behaviour is role-played from the prior [116, 120], and still happens [55, 56]. The evidence on whether RL training raises it is mixed: He et al. find RL-trained models more instrumental [118]; Alparslan et al. find no monotone effect across RLVR checkpoints [119].
- Planning survives only in CHAT-P, where the PRM over a deterministic tree is AlphaZero's shape [59]. AGENT-X has horizon without a model, which is the worst quadrant for RL theory.
- The contract view [63] makes the stacking explicit: RL assumes a complete contract; every LLM column has an incomplete one filled by the prior; the agent has three incomplete contracts and no party present to renegotiate.
- The behavior-culture incidents in `../llm-agent-incident-catalog/incidents/catalog.csv` sit in AGENT-A and AGENT-X. The RL-safety constructions sit in RL and CHAT-P. The two cultures are, in this table, looking at different columns.

## 7. Provenance of citations

- References 1–67 were checked on 2026-11-21 by automated retrieval of each URL, comparing title, first author, year and venue. Result: 63 correct, 4 corrected (21, 23, 38, 43: venue or proceedings year), 4 optional venue additions applied (16, 20, 26, 61), 0 not found.
- References 68–124 were added in the same pass, each retrieved when proposed; two (76, 122) were taken from search results without the page being opened.
- The priority check searched for prior statements of six claims in §6. Verdicts: KL-as-constraint known [73, 19, 12]; bandit framing and critic-dropping known [17, 70–72]; PRM retreat known, ranking of settings not found; identifiability rungs 1–2 known, 3 informal, 4 not found; instrumental-behaviour components known separately, evidence mixed [118, 119]; McLean-classes-to-settings mapping not found.
- Citations are not independently verified by a human.

## References

1. Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html
2. Kaelbling, L. P., Littman, M. L. & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence* 101(1–2), 99–134. https://doi.org/10.1016/S0004-3702(98)00023-X
3. Altman, E. (1999). *Constrained Markov Decision Processes*. Chapman & Hall/CRC. https://www.taylorfrancis.com/books/mono/10.1201/9781315140223/constrained-markov-decision-processes-eitan-altman
4. Amodei, D. et al. (2016). Concrete problems in AI safety. https://arxiv.org/abs/1606.06565
5. Skalse, J. et al. (2022). Defining and characterizing reward gaming. *NeurIPS*. https://arxiv.org/abs/2209.13085
6. García, J. & Fernández, F. (2015). A comprehensive survey on safe reinforcement learning. *JMLR* 16, 1437–1480. http://jmlr.org/papers/v16/garcia15a.html
7. Alshiekh, M. et al. (2018). Safe reinforcement learning via shielding. *AAAI*. https://arxiv.org/abs/1708.08611
8. Sharma, A. et al. (2022). Autonomous reinforcement learning: formalism and benchmarking. *ICLR*. https://arxiv.org/abs/2112.09605
9. Grinsztajn, N. et al. (2021). There is no turning back: a self-supervised approach for reversibility-aware reinforcement learning. *NeurIPS*. https://arxiv.org/abs/2106.04480
10. Zhao, W., Queralta, J. P. & Westerlund, T. (2020). Sim-to-real transfer in deep reinforcement learning for robotics: a survey. *IEEE SSCI*. https://arxiv.org/abs/2009.13303
11. Christiano, P. et al. (2017). Deep reinforcement learning from human preferences. *NeurIPS*. https://arxiv.org/abs/1706.03741
12. Ziegler, D. M. et al. (2019). Fine-tuning language models from human preferences. https://arxiv.org/abs/1909.08593
13. Stiennon, N. et al. (2020). Learning to summarize from human feedback. *NeurIPS*. https://arxiv.org/abs/2009.01325
14. Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS*. https://arxiv.org/abs/2203.02155
15. Rafailov, R. et al. (2023). Direct Preference Optimization: your language model is secretly a reward model. *NeurIPS*. https://arxiv.org/abs/2305.18290
16. Rafailov, R. et al. (2024). From r to Q*: your language model is secretly a Q-function. *COLM*. https://arxiv.org/abs/2404.12358
17. Ahmadian, A. et al. (2024). Back to basics: revisiting REINFORCE-style optimization for learning from human feedback in LLMs. *ACL*. https://arxiv.org/abs/2402.14740
18. Shao, Z. et al. (2024). DeepSeekMath: pushing the limits of mathematical reasoning in open language models (GRPO). https://arxiv.org/abs/2402.03300
19. Gao, L., Schulman, J. & Hilton, J. (2023). Scaling laws for reward model overoptimization. *ICML*. https://arxiv.org/abs/2210.10760
20. Singhal, P. et al. (2024). A long way to go: investigating length correlations in RLHF. *COLM*. https://arxiv.org/abs/2310.03716
21. Sharma, M. et al. (2024). Towards understanding sycophancy in language models. *ICLR*. https://arxiv.org/abs/2310.13548
22. Lambert, N. et al. (2024). Tülu 3: pushing frontiers in open language model post-training (RLVR). https://arxiv.org/abs/2411.15124
23. DeepSeek-AI (2025). DeepSeek-R1: incentivizing reasoning capability in LLMs via reinforcement learning. *Nature* 645, 633–638. https://arxiv.org/abs/2501.12948
24. Baker, B. et al. (2025). Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. https://arxiv.org/abs/2503.11926
25. Uesato, J. et al. (2022). Solving math word problems with process- and outcome-based feedback. https://arxiv.org/abs/2211.14275
26. Lightman, H. et al. (2024). Let's verify step by step. *ICLR*. https://arxiv.org/abs/2305.20050
27. Wang, P. et al. (2024). Math-Shepherd: verify and reinforce LLMs step-by-step without human annotations. *ACL*. https://arxiv.org/abs/2312.08935
28. Zhang, Z. et al. (2025). The lessons of developing process reward models in mathematical reasoning. https://arxiv.org/abs/2501.07301
29. Snell, C. et al. (2024). Scaling LLM test-time compute optimally can be more effective than scaling model parameters. https://arxiv.org/abs/2408.03314
30. Brown, B. et al. (2024). Large language monkeys: scaling inference compute with repeated sampling. https://arxiv.org/abs/2407.21787
31. Yao, S. et al. (2023). Tree of Thoughts: deliberate problem solving with large language models. *NeurIPS*. https://arxiv.org/abs/2305.10601
32. Ross, S., Gordon, G. & Bagnell, J. A. (2011). A reduction of imitation learning and structured prediction to no-regret online learning (DAgger). *AISTATS*. https://arxiv.org/abs/1011.0686
33. Turpin, M. et al. (2023). Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting. *NeurIPS*. https://arxiv.org/abs/2305.04388
34. Lanham, T. et al. (2023). Measuring faithfulness in chain-of-thought reasoning. https://arxiv.org/abs/2307.13702
35. Yao, S. et al. (2023). ReAct: synergizing reasoning and acting in language models. *ICLR*. https://arxiv.org/abs/2210.03629
36. Schick, T. et al. (2023). Toolformer: language models can teach themselves to use tools. *NeurIPS*. https://arxiv.org/abs/2302.04761
37. Greshake, K. et al. (2023). Not what you've signed up for: compromising real-world LLM-integrated applications with indirect prompt injection. *AISec*. https://arxiv.org/abs/2302.12173
38. Zverev, E. et al. (2025). Can LLMs separate instructions from data? And what do we even mean by that? *ICLR*. https://arxiv.org/abs/2403.06833
39. Wallace, E. et al. (2024). The instruction hierarchy: training LLMs to prioritize privileged instructions. https://arxiv.org/abs/2404.13208
40. Debenedetti, E. et al. (2024). AgentDojo: a dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. *NeurIPS*. https://arxiv.org/abs/2406.13352
41. Chen, Z. et al. (2024). AgentPoison: red-teaming LLM agents via poisoning memory or knowledge bases. *NeurIPS*. https://arxiv.org/abs/2407.12784
42. Jimenez, C. E. et al. (2024). SWE-bench: can language models resolve real-world GitHub issues? *ICLR*. https://arxiv.org/abs/2310.06770
43. Wei, Y. et al. (2025). SWE-RL: advancing LLM reasoning via reinforcement learning on open software evolution. *NeurIPS*. https://arxiv.org/abs/2502.18449
44. Kapoor, S. et al. (2024). AI agents that matter. https://arxiv.org/abs/2407.01502
45. Shavit, Y. et al. (2023). Practices for governing agentic AI systems. OpenAI. https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf
46. Chan, A. et al. (2023). Harms from increasingly agentic algorithmic systems. *FAccT*. https://arxiv.org/abs/2302.10329
47. Hammond, L. et al. (2025). Multi-agent risks from advanced AI. https://arxiv.org/abs/2502.14143
48. Laine, R. et al. (2024). Me, myself, and AI: the Situational Awareness Dataset (SAD) for LLMs. *NeurIPS*. https://arxiv.org/abs/2407.04694
49. Greenblatt, R. et al. (2024). Alignment faking in large language models. https://arxiv.org/abs/2412.14093
50. OpenAI (2024–). Model Spec. https://model-spec.openai.com/
51. Pan, A., Bhatia, K. & Steinhardt, J. (2022). The effects of reward misspecification: mapping and mitigating misaligned models. *ICLR*. https://arxiv.org/abs/2201.03544

52. Ng, A. Y. & Russell, S. (2000). Algorithms for inverse reinforcement learning. *ICML*. https://ai.stanford.edu/~ang/papers/icml00-irl.pdf
53. Skalse, J. et al. (2023). Invariance in policy optimisation and partial identifiability in reward learning. *ICML*. https://arxiv.org/abs/2203.07475
54. Turner, A. M. et al. (2021). Optimal policies tend to seek power. *NeurIPS*. https://arxiv.org/abs/1912.01683
55. Meinke, A. et al. (2024). Frontier models are capable of in-context scheming. https://arxiv.org/abs/2412.04984
56. Lynch, A. et al. (2025). Agentic misalignment: how LLMs could be insider threats. Anthropic. https://www.anthropic.com/research/agentic-misalignment
57. Denison, C. et al. (2024). Sycophancy to subterfuge: investigating reward-tampering in large language models. https://arxiv.org/abs/2406.10162
58. Schrittwieser, J. et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero). *Nature* 588. https://arxiv.org/abs/1911.08265
59. Silver, D. et al. (2017). Mastering chess and shogi by self-play with a general reinforcement learning algorithm (AlphaZero). https://arxiv.org/abs/1712.01815
60. Hao, S. et al. (2023). Reasoning with language model is planning with world model (RAP). *EMNLP*. https://arxiv.org/abs/2305.14992
61. Yue, Y. et al. (2025). Does reinforcement learning really incentivize reasoning capacity in LLMs beyond the base model? *NeurIPS*. https://arxiv.org/abs/2504.13837
62. Shao, R. et al. (2025). Spurious rewards: rethinking training signals in RLVR. https://arxiv.org/abs/2506.10947
63. Hadfield-Menell, D. & Hadfield, G. K. (2019). Incomplete contracting and AI alignment. *AIES*. https://arxiv.org/abs/1804.04268
64. Kasirzadeh, A. & Gabriel, I. (2025). Characterizing AI agents for alignment and governance. https://arxiv.org/abs/2504.21848
65. Mitchell, M. et al. (2025). Fully autonomous AI agents should not be developed. https://arxiv.org/abs/2502.02649
66. Debenedetti, E. et al. (2025). Defeating prompt injections by design (CaMeL). https://arxiv.org/abs/2503.18813
67. Korbak, T. et al. (2025). Chain of thought monitorability: a new and fragile opportunity for AI safety. https://arxiv.org/abs/2507.11473

68. Schulman, J., Wolski, F., Dhariwal, P., Radford, A. & Klimov, O. (2017). Proximal policy optimization algorithms. https://arxiv.org/abs/1707.06347
69. Schulman, J., Levine, S., Moritz, P., Jordan, M. I. & Abbeel, P. (2015). Trust region policy optimization. *ICML*. https://arxiv.org/abs/1502.05477
70. Li, Z. et al. (2024). ReMax: a simple, effective, and efficient reinforcement learning method for aligning large language models. *ICML*. https://arxiv.org/abs/2310.10505
71. Xiong, W. et al. (2024). Iterative preference learning from human feedback: bridging theory and practice for RLHF under KL-constraint. *ICML*. https://arxiv.org/abs/2312.11456
72. Lambert, N. (2025). *Reinforcement Learning from Human Feedback*. https://arxiv.org/abs/2504.12501
73. Moskovitz, T. et al. (2024). Confronting reward model overoptimization with constrained RLHF. *ICLR*. https://arxiv.org/abs/2310.04373
74. Korbak, T., Perez, E. & Buckley, C. L. (2022). RL with KL penalties is better viewed as Bayesian inference. *Findings of EMNLP*. https://arxiv.org/abs/2205.11275
75. Jaques, N. et al. (2017). Sequence Tutor: conservative fine-tuning of sequence generation models with KL-control. *ICML*. https://arxiv.org/abs/1611.02796
76. Ng, A. Y., Harada, D. & Russell, S. (1999). Policy invariance under reward transformations: theory and application to reward shaping. *ICML*. https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf
77. Bowling, M., Martin, J. D., Abel, D. & Dabney, W. (2023). Settling the reward hypothesis. *ICML*. https://arxiv.org/abs/2212.10420
78. Everitt, T., Hutter, M., Kumar, R. & Krakovna, V. (2021). Reward tampering problems and solutions in reinforcement learning: a causal influence diagram perspective. *Synthese*. https://arxiv.org/abs/1908.04734
79. Casper, S. et al. (2023). Open problems and fundamental limitations of reinforcement learning from human feedback. *TMLR*. https://arxiv.org/abs/2307.15217
80. MacDiarmid, M. et al. (2025). Natural emergent misalignment from reward hacking in production RL. https://arxiv.org/abs/2511.18397
81. Cobbe, K. et al. (2021). Training verifiers to solve math word problems. https://arxiv.org/abs/2110.14168
82. Kirk, R. et al. (2024). Understanding the effects of RLHF on LLM generalisation and diversity. *ICLR*. https://arxiv.org/abs/2310.06452
83. Bellemare, M. G. et al. (2016). Unifying count-based exploration and intrinsic motivation. *NeurIPS*. https://arxiv.org/abs/1606.01868
84. Achiam, J., Held, D., Tamar, A. & Abbeel, P. (2017). Constrained policy optimization. *ICML*. https://arxiv.org/abs/1705.10528
85. Levine, S., Kumar, A., Tucker, G. & Fu, J. (2020). Offline reinforcement learning: tutorial, review, and perspectives on open problems. https://arxiv.org/abs/2005.01643
86. Tobin, J. et al. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. *IROS*. https://arxiv.org/abs/1703.06907
87. Shinn, N. et al. (2023). Reflexion: language agents with verbal reinforcement learning. *NeurIPS*. https://arxiv.org/abs/2303.11366
88. Zhou, A. et al. (2024). Language agent tree search unifies reasoning, acting, and planning in language models. *ICML*. https://arxiv.org/abs/2310.04406
89. Zhou, Y., Zanette, A., Pan, J., Levine, S. & Kumar, A. (2024). ArCHer: training language model agents via hierarchical multi-turn RL. *ICML*. https://arxiv.org/abs/2402.19446
90. Feng, X. et al. (2023). AlphaZero-like tree-search can guide large language model decoding and training. https://arxiv.org/abs/2309.17179
91. Gao, J. et al. (2024). On designing effective RL reward at training time for LLM reasoning. https://arxiv.org/abs/2410.15115
92. Feng, Z. et al. (2025). Is PRM necessary? Problem-solving RL implicitly induces PRM capability in LLMs. https://arxiv.org/abs/2505.11227
93. Huang, Y. et al. (2025). Pitfalls of rule- and model-based verifiers: a case study on mathematical reasoning. https://arxiv.org/abs/2505.22203
94. Kwa, T. et al. (2025). Measuring AI ability to complete long software tasks. *NeurIPS*. https://arxiv.org/abs/2503.14499
95. Yao, S., Shinn, N., Razavi, P. & Narasimhan, K. (2024). τ-bench: a benchmark for tool-agent-user interaction in real-world domains. https://arxiv.org/abs/2406.12045
96. Ruan, Y. et al. (2024). Identifying the risks of LM agents with an LM-emulated sandbox (ToolEmu). *ICLR*. https://arxiv.org/abs/2309.15817
97. Krakovna, V., Orseau, L., Kumar, R., Martic, M. & Legg, S. (2018). Penalizing side effects using stepwise relative reachability. https://arxiv.org/abs/1806.01186
98. Turner, A. M., Hadfield-Menell, D. & Tadepalli, P. (2020). Conservative agency via attainable utility preservation. *AIES*. https://arxiv.org/abs/1902.09725
99. Eysenbach, B., Gu, S., Ibarz, J. & Levine, S. (2018). Leave no trace: learning to reset for safe and autonomous reinforcement learning. *ICLR*. https://arxiv.org/abs/1711.06782
100. Pinto, L., Davidson, J., Sukthankar, R. & Gupta, A. (2017). Robust adversarial reinforcement learning. *ICML*. https://arxiv.org/abs/1703.02702
101. Lowe, R. et al. (2017). Multi-agent actor-critic for mixed cooperative-competitive environments. *NeurIPS*. https://arxiv.org/abs/1706.02275
102. Leike, J. et al. (2017). AI safety gridworlds. https://arxiv.org/abs/1711.09883
103. Hadfield-Menell, D., Dragan, A., Abbeel, P. & Russell, S. (2016). Cooperative inverse reinforcement learning. *NeurIPS*. https://arxiv.org/abs/1606.03137
104. Hadfield-Menell, D., Dragan, A., Abbeel, P. & Russell, S. (2017). The off-switch game. *IJCAI*. https://arxiv.org/abs/1611.08219
105. Wei, A., Haghtalab, N. & Steinhardt, J. (2023). Jailbroken: how does LLM safety training fail? *NeurIPS*. https://arxiv.org/abs/2307.02483
106. Zou, A. et al. (2023). Universal and transferable adversarial attacks on aligned language models. https://arxiv.org/abs/2307.15043
107. Zhan, Q., Liang, Z., Ying, Z. & Kang, D. (2024). InjecAgent: benchmarking indirect prompt injections in tool-integrated large language model agents. *Findings of ACL*. https://arxiv.org/abs/2403.02691
108. Cemri, M. et al. (2025). Why do multi-agent LLM systems fail? (MAST). https://arxiv.org/abs/2503.13657
109. Bai, Y. et al. (2022). Constitutional AI: harmlessness from AI feedback. https://arxiv.org/abs/2212.08073
110. Inan, H. et al. (2023). Llama Guard: LLM-based input-output safeguard for human-AI conversations. https://arxiv.org/abs/2312.06674
111. Guan, M. Y. et al. (2024). Deliberative alignment: reasoning enables safer language models. https://arxiv.org/abs/2412.16339
112. Chen, Y. et al. (2025). Reasoning models don't always say what they think. https://arxiv.org/abs/2505.05410
113. Greenblatt, R., Shlegeris, B., Sachan, K. & Roger, F. (2024). AI control: improving safety despite intentional subversion. *ICML*. https://arxiv.org/abs/2312.06942
114. Zhang, Z. et al. (2024). Agent-SafetyBench: evaluating the safety of LLM agents. https://arxiv.org/abs/2412.14470
115. Feng, K. J. K., McDonald, D. W. & Zhang, A. X. (2025). Levels of autonomy for AI agents. https://arxiv.org/abs/2506.12469
116. Shanahan, M., McDonell, K. & Reynolds, L. (2023). Role play with large language models. *Nature* 623, 493–498. https://arxiv.org/abs/2305.16367
117. Turner, A. M. & Tadepalli, P. (2022). Parametrically retargetable decision-makers tend to seek power. *NeurIPS*. https://arxiv.org/abs/2206.13477
118. He, Y. et al. (2025). Evaluating the paperclip maximizer: are RL-based language models more likely to pursue instrumental goals? https://arxiv.org/abs/2502.12206
119. Alparslan, B. et al. (2026). Questioning instrumental convergence in RLVR: checkpoint evidence from OLMo-3. https://arxiv.org/abs/2610.31624
120. Tice, C. et al. (2026). Alignment pretraining: AI discourse causes self-fulfilling (mis)alignment. https://arxiv.org/abs/2601.10160
121. Sheshadri, A. et al. (2025). Why do some language models fake alignment while others don't? https://arxiv.org/abs/2506.18032
122. Ng, A. W. et al. (2026). Agent safety should be a runtime contract. https://arxiv.org/abs/2608.11274
123. Cagatan, O. V. & Zhao, X. (2026). Reward hacking in language model agents: revisiting AI Safety Gridworlds. https://arxiv.org/abs/2606.15385
124. Zelikman, E., Wu, Y., Mu, J. & Goodman, N. D. (2022). STaR: bootstrapping reasoning with reasoning. *NeurIPS*. https://arxiv.org/abs/2203.14465
