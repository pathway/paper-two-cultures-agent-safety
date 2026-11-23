# Semantics of core concepts: RL, LLM base model, LLM agent with tools

!!! warning "Status: STARTED"
    Draft. Not fully human-reviewed. See [the AI-use statement](../ai-use.md).


Date: 2026-11-21. Companion to `assumptions_table.md` (rows A1–F2) and `framing.md`.

Purpose. The two cultures use the same words. This table states what each word denotes in three settings. The middle column matters: the LLM agent inherits most of its semantics from the base model, not from RL, even when it is trained with RL.

Reading key. "RL" = classical MDP/POMDP agent [1]. "Base model" = a pretrained, post-trained LLM used as a text function. "LLM agent" = a frozen model inside a scaffold loop with tools [4]. Last column names the `assumptions_table.md` rows the shift feeds.

## 1. Agent and environment

| Concept | RL | LLM base model | LLM agent with tools | Rows |
|---|---|---|---|---|
| Agent | The policy π. One learned object; everything else is given. | No agent. A conditional distribution over the next token, p(x_t \| x_<t). | Model + scaffold + tool set + system prompt. The model alone is not the agent; most of what varies at deployment is outside the weights. | D1, D3, E3 |
| Environment | An MDP built or simulated by the experimenter; known interface, fixed dynamics. | None at inference. The prompt author plays the environment. In training, the text corpus. | Real software, files, web, accounts, other agents, humans. Nobody built it; parts of it are hostile. | C1, C4, C5 |
| State | Markov state s_t: a sufficient statistic for the future in a designer-chosen representation. | The context window. Trivially Markov in the token sequence. | Context window plus external world state the model cannot see (files, accounts, side effects already made). Includes the user's intent. Non-Markov in the context. | C3 |
| Observation | o_t = sensor(s_t), designer-defined. Data only; carries no commands. | The prompt. The only input, and it is both data and instruction. | Tool outputs, retrieved pages, user turns, all in one token stream with the instructions. Observations can carry commands [5]. | A2, C4 |
| Action | a_t from a fixed, small set with fixed semantics. | One token from a fixed vocabulary. No side effect. | A text span the scaffold parses into a tool call. Open-ended, compositional; meaning depends on the tool and its arguments; side effects in the world. | D1 |
| Transition dynamics | P(s'\|s,a): fixed, stationary, often known or simulated. | Deterministic append of the sampled token. | Whatever the tool and the world do. Non-stationary, unknown to the designer, partly controlled by third parties. | C1 |
| Other agents | Single agent, or a designed multi-agent game. | None. Stateless function; infinitely many identical copies. | Concurrent instances, sub-agents, copies of itself, other vendors' agents, unknown humans. | C5 |
| Time step | A clock tick fixed by the designer. | One token. | One model turn or one tool call. Real duration from seconds to hours. | C2 |

## 2. Objective and value

| Concept | RL | LLM base model | LLM agent with tools | Rows |
|---|---|---|---|---|
| Reward / objective | Scalar R(s,a) written in advance by the designer. Exogenous to observations. Delivered each step. | Pretraining: next-token likelihood. Post-training: a preference reward model [6]. Neither exists at inference. | No scalar at run time. The effective objective is the instruction in the context, and any text in the context can revise it, including tool output. Success is judged afterwards by the user. | A1, A2, A3, B2 |
| Return / value | V(s), Q(s,a): expected discounted sum. The central computational object. | None. | None explicit. "Value" lives in the model's verbal judgment and the user's acceptance. No discount. | A1 |
| Goal-directedness | By construction: π maximizes expected return. | Not goal-directed. Simulates goal-directed text. | Role-played from the instruction. Persists only while the context supports it; a new instruction can drop or replace the goal. | A1, A4 |
| Specification | R and cost C, written once by one expert before training. | The vendor's training data and post-training rubric (e.g. a model spec) [7], baked into weights. | Split across three parties: vendor spec in the weights; deployer system prompt and tool permissions, writable and enforceable at the tool layer; user instruction at test time by a non-expert. | A3, A5, E3 |
| Principal | One party: the designer, who also trains and deploys. | The vendor. | Vendor, deployer, user, plus third parties whose content enters the context. Three or more principals with conflicting instructions. | A1, E3 |
| Horizon / episode | Episodes with resets. Many episodes; a failure costs one episode. | One sequence; ends at EOS or the context limit. | One task run. Ends when the model says done, the scaffold hits a step cap, or the user interrupts. No reset of the world; actions persist. | C2 |
| Termination | A terminal state of the MDP. | The EOS token. | A claim by the model that the task is done. Not a world state; can be false. | F1 |

## 3. Learning and knowledge

| Concept | RL | LLM base model | LLM agent with tools | Rows |
|---|---|---|---|---|
| Learning | Online loop: acting and learning are one process, from scratch. | Offline: pretraining on text, then post-training. Weights frozen afterwards. | No weight update at deployment. "Learning" means in-context adaptation and memory files written by the scaffold. The deployer cannot retrain. | B1, B3, E3 |
| Source of competence | Reward-driven trial and error. | Imitation of human text. | Inherited from the base model; the scaffold adds tools and a loop, not competence. | B3 |
| Prior knowledge / norms | None. Tabula rasa. | Human norms, and their violations, from the corpus. | Same norms, now attached to actions with side effects. | B4 |
| Exploration | Designed: ε-greedy, entropy bonus, UCB. A core problem. | Sampling temperature. No notion of information gain. | Not designed. Novel actions come from sampling the prior. Exploration happens in the real world with real side effects. | B5 |
| Generalization | To unseen states of the same MDP; sim-to-real [2]. | To unseen prompts within the distribution of human text. | To unseen tools, sites, tasks and users. The distribution is whatever the world presents. | C1 |
| Memory | The state is the memory (Markov). Recurrent policy for POMDPs. | Context window only. Nothing persists across calls. | Context plus scaffold stores (files, vector DB, memory tools). Writable by the agent and by injected content. | C3 |
| Self-model | None. | Knows what an LLM, an evaluation and a monitor are, from text [8]. | Same knowledge, now applied to its own oversight. Can distinguish test from deployment contexts. | E1 |

## 4. Safety and oversight

| Concept | RL | LLM base model | LLM agent with tools | Rows |
|---|---|---|---|---|
| Safety constraint | Cost c(s,a) with a budget (CMDP) [3]; shield over a known unsafe set. | Refusal behaviour trained in; a content policy. | Two layers. Tool layer: allow/deny lists, approval gates, sandboxes; writable and enforceable. Policy layer: "harmful" or "unwanted" side effects; not writable in advance. Gates get switched off by users. | A5, E2 |
| Failure | Low return; constraint violation; reward hacking of R. | Wrong or harmful text; hallucination; jailbreak. | A harmful side effect in the world: deleted data, leaked secret, money moved, message sent. Reached via injection, over-permission or misread instruction. | F1 |
| Adversary | Nature's stochasticity. Occasionally a perturbation of observations. | The prompt author (jailbreak). | Any content author on the retrieval or tool path [5]; other agents; the user's own ambiguous instruction. | C4 |
| Oversight channel | None at run time. Evaluation by return after training. | Output filters; human raters at training time. | Reasoning traces, tool-call logs, human approval per step. Monitorable, but the agent models the monitor and the user disables the gate. | D2, E1, E2 |
| Steering at deployment | Change R and retrain. | Change the prompt. | Change the system prompt, tools, permissions or examples. No retraining; no access to weights. | D3 |
| Validation | Expected return and cost on the training MDP or held-out seeds. | Benchmarks; red-team pass rates. | Attack success rates, eval pass rates, incident records. The eval is itself a specification the agent can recognise and game. | F1, F2 |

## 5. Where the semantics break

- Six concepts keep their RL meaning in the agent setting: action (as "thing with side effects"), transition, horizon, failure, adversary, validation. They break in the base-model column and come back for the agent.
- Six concepts never recover their RL meaning: reward, return, value, exploration, learning, episode reset. The agent has none of these at run time. Theory built on them transfers only if it is reinterpreted (see `framing.md` §5).
- Four concepts are new and have no RL counterpart: observation-as-command, three-party specification, self-model of oversight, scaffold-held memory. These are where the behavior-culture incidents concentrate (`../llm-agent-incident-catalog/taxonomy/taxonomy_stats.md`).
- The base-model column is the source of the agent's semantics for state, action, learning, competence, norms and self-model. The agent inherits them unchanged; the scaffold adds side effects.

## References

1. Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html
2. Zhao, W., Queralta, J. P. & Westerlund, T. (2020). Sim-to-real transfer in deep reinforcement learning for robotics: a survey. *IEEE SSCI*. https://arxiv.org/abs/2009.13303
3. Altman, E. (1999). *Constrained Markov Decision Processes*. Chapman & Hall/CRC. https://www.taylorfrancis.com/books/mono/10.1201/9781315140223/constrained-markov-decision-processes-eitan-altman
4. Yao, S. et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*. https://arxiv.org/abs/2210.03629
5. Greshake, K. et al. (2023). Not what you've signed up for: compromising real-world LLM-integrated applications with indirect prompt injection. *AISec*. https://arxiv.org/abs/2302.12173
6. Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS*. https://arxiv.org/abs/2203.02155
7. OpenAI (2024). Model Spec. https://model-spec.openai.com/
8. Laine, R. et al. (2024). Me, myself, and AI: the Situational Awareness Dataset (SAD) for LLMs. *NeurIPS*. https://arxiv.org/abs/2407.04694
