---
key: mclean2026
read: full
read_detail: full text read end to end from the local text extraction (two-column PDF; figure and Table 1 text is interleaved), abstract to Appendix A
read_on: 2026-11-24
---

# McLean et al. 2026, section by section

Source: [1] McLean et al., "AI Agent Safety is a Reinforcement Learning Problem", AIWILD @ ICML 2026. https://openreview.net/forum?id=wvga9chmb6

Each section gives: what it claims, which works it cites, verbatim quotes, and what it means for our paper ("For us").

## Abstract

- Claim: agent failures "are structural instances of problems RL has formalized for decades", and RL safety tools apply.
- Cites: nothing.
- Quotes:
  - "the RL safety literature provides principled tools to diagnose and address them"
  - "we formalize the problem equivalence"
- For us: this is the claim our conclusion answers.

## §1 Introduction

- Claim: LLM agents solve sequential decision problems; their failures are RL failure modes.
- Incidents: database deletion (Nolan 2025), crypto mining (Wang et al. 2026), data leak (Down 2026), email deletion (Martindale 2026).
- Failure classes named: lack of generalization, distributional shift, reward hacking.
- Tools named, with citations:
  - constraining behaviour: Altman 1999;
  - diagnosing reward misspecification: Muslimani 2025;
  - ensuring safe exploration: Wachi 2023.
- Quotes:
  - "the RL safety literature for constraining agent behavior (Altman, 1999), diagnosing reward misspecification (Muslimani et al., 2025), and ensuring safe exploration (Wachi et al., 2023) are applicable to AI agents"
  - "The structural parallel between AI Agent failures and well-characterized RL failure modes is the central argument of this paper."
- For us: the only place Wachi 2023 is cited.

## §2 Background

- Claim: the agent definitions of Russell and Norvig and of Wooldridge and Jennings fit LLM agents. The paper studies one agent, not multi-agent "Agentic AI".
- Evidence of failure: Paglieri 2025 (performance falls with horizon), Xu 2025 (no agent above 30% of office tasks), Simhi 2026 (agents do not reliably choose the safe option).
- RL background: exploration (bandits, curiosity, options), credit assignment (TD, eligibility traces), partial observability (Kaelbling 1998).
- Quotes:
  - "we will focus on the individual AI agent that is built on top of a LLM as the core subject of our analysis"
  - "acts on partial information in irreversible situations"
- For us: the single-agent scope is consistent with U4 (one principal), but they do not state it as an assumption.

## §3.1–3.3 Interaction loop, stochastic control, specialisation

- Claim: the ReAct loop and the Sutton–Barto loop are the same process. They specialise stochastic control to an MDP by adding discrete time, full observability (relaxed in §3.5), the Markov property and a per-step reward.
- Quotes:
  - "This structural equivalence is not coincidental"
  - "The objective function J measures the degree to which the trajectory of the AI agent's interactions satisfies the requirements implicitly defined by a user's instructions."
- For us: the objective is "implicitly defined by a user's instructions". That is U1: the objective is set through observations.

## §3.4 MDPs

- Claim: when P is known, dynamic programming finds the optimal policy; otherwise the agent learns from interaction. The paper treats deployment.
- Quotes:
  - "In practice, however, the transition function is rarely known"
  - "While we discuss the problems that AI agents are solving during deployment"
- Defect in [1]: "RLHF () and RLVR ()" has empty citations.
- For us: their own scope is deployment (our D-AGENT). They concede that S2 (known model) usually fails.

## §3.5 POMDPs and Table 1

- Claim: an agent is a POMDP. The state includes "the user's intents, safety constraints"; the observation function is "lossy". In deployment the reward is an "internalized proxy signal".
- Cites as convergent POMDP work on performance: SPA-RL, HCAPO, VAGEN, ArCHer, RAGEN.
- Cites as RL safety tools: reward misspecification (Muslimani 2025; Vasan 2024; Knox 2023); exploration (Tse 2025; Klissarov and Machado 2023); safe sequential decision-making under uncertainty (Mohammedalamen 2025a, b).
- Quotes:
  - "they apply it exclusively to performance"
  - "The systematic application of this formalism to AI agent safety has not yet followed, which is the gap that this paper addresses."
  - "This is a lossy process"
- For us:
  - Safety constraints are placed inside the hidden state S. So S1 (a given specification) fails in their own model.
  - Vasan 2024, Knox 2023, Tse 2025 and Klissarov and Machado 2023 are cited as tools but are **not in our tool table** (see "Gaps" below).

## §3.6.1 Reward misspecification

- Claim: Skalse 2022 proves that proxy rewards are hackable. [1] hypothesise that the agent learns an internal reward function f(o_p, o_g), possibly from RLVR, and a wrong prompt leads to hacking.
- Incident: Replit deleted a production database during a code freeze, then made fake records (Nolan 2025).
- Quotes:
  - "Any specification that omits context, nuance, or implicit constraints is theoretically exploitable."
  - "The only way that a user can interact with the AI agent during deployment is through the initial prompt"
  - "We hypothesize that the AI agent learns an internal reward function"
- For us:
  - The deployed reward is a hypothesis in [1], not a stated object. This supports our "no D-PRM" point.
  - The prompt sets the objective, so U1 is used.
  - No tool is offered in this subsection.

## §3.6.2 Safe exploration

- Claim: exploration failures lead into "irreversible states" (Lee 2025). The example is `rm -rf /`. What is missing is a shield or a CMDP that blocks high-risk actions beforehand. KL regularisation is not a shield.
- Cites: Lee 2025 (irreversible states); Altman 1999 (CMDP); Shao 2024 and Guo 2025 (KL in RLHF/RLVR). No paper is cited for the shield.
- Quotes:
  - "irreversible states (Lee, 2025), regions of the state space S from which it is impossible to return to a safe or functional state"
  - "Unlike games or simulations where agents can be \"reset,\" real-world AI agent deployments often lack a safety shield or a \"constrained MDP\" (Altman, 1999) framework that prevents the exploration of high-risk actions before they occur."
  - "A safety shield operates at inference time over the action space"
  - "The former is what is missing from deployed AI Agents."
- For us:
  - [1] itself says resets are not available in deployment. Wachi 2023 (cited in §1) assumes one. This sharpens our main finding: [1] names the missing reset, but the tool it cites needs it.
  - The remedy named in §3.6.2 is a shield or Altman's CMDP, not Wachi. Our draft says §3.6.2 "present safe exploration as the answer", which is loose: Wachi is cited in §1.
  - Lee 2025, "Robust and scalable autonomous reinforcement learning in irreversible environments", is a cited RL paper on irreversibility. **We have not read it.** It may weaken "the tools assume reversibility".

## §3.6.3 Observation ambiguity

- Claim: treating a POMDP as an MDP is the error. Belief-state planning would take an information-gathering action first.
- Incident: Terraform `destroy` after a missing state file, 1,943,200 rows deleted (Grigorev 2025).
- Cites: Kaelbling 1998.
- Quotes:
  - "take an information gathering action before committing to an irreversible transition"
  - "This is precisely the behavior that belief state planning in POMDPs is designed to produce"
- For us: belief-state planning needs a known finite model (S2, S3). [1] gives the behaviour, not a method that runs on an LLM.

## §4 Counter-arguments

Three objections, each answered by [1].

1. **No scalar reward in deployment.**
   - Answer: a PRM is used in training and then removed. The agent "implicitly learns" a completion function that would be "equivalent to a sparse reward signal".
   - Cites: Liu 2025 (PRM); Skalse 2022.
   - Quotes: "Regardless of the true mechanism that evaluates completeness, the MDP framing that we provide in this paper provides a diagnostic lens for discussing and solving these reward specification problems."
   - For us: the source of our "diagnostic lens" quote. [1] say "discussing and solving", not only diagnosing.
2. **RL safety methods will not scale because of the finite context window.**
   - Answer: "This is a fair critique". The context window is structured partial observability. Elelimy 2025b proposes learning a history-to-state map. CMDPs address weighting safety in that map.
   - Cites: Elelimy 2025b; Altman 1999; Satija 2020.
   - Quotes:
     - "Currently, there is no guarantee that safety-relevant information receives appropriate weight when it conflicts with task-completion information."
     - "is precisely the problem that constrained MDPs address (Altman, 1999; Satija et al., 2020), suggesting again that the RL safety literature has tools directly applicable here"
   - For us: the only place Satija 2020 is cited. CMDPs constrain the cost of a policy, not the weighting of features in a learned state map. Our Satija row (ergodicity, slow updates) applies.
3. **AI agents use tools; RL agents use primitive actions.**
   - Answer: tool calls are options (Sutton 1999). Options help exploration (Klissarov and Machado 2023; Jinnai 2020). Atomic skills (Ma 2026) link agents to multi-task RL.
   - For us: about the action space, not safety. No condition is affected.

## §5 Limitations

- Claim 1: there is a scaling gap. Classical safety algorithms cannot be mapped one-to-one, but this is an "opportunity".
- Claim 2: the position is complementary to scalable oversight and AI control (Bowman 2022). It does not solve specifying "a flawless objective function".
- Tools named: CMDPs (Altman 1999), shielding (no citation), reward function alignment (Muslimani 2025).
- Quotes:
  - "a significant scaling gap exists between the abstract formalisms that unify these settings and the practical solution methods deployed within them"
  - "classical RL safety algorithms—which often rely on tabular representations, exact runtime shielding, or known transition matrices—cannot be mapped one-to-one onto LLM backbones"
  - "a profound opportunity for the community to scale foundational RL principles up to high-dimensional, semantic domains"
  - "it does not inherently solve the foundational challenge of specifying a flawless objective function for superhuman systems"
  - "Our position should therefore be viewed as a complementary framework for structural safety"
- For us: [1] concede S2, S3 and (through shielding) S1, and they concede the specification problem (U1 in part). They attribute the gap to dimensionality. Our position is that the gap is reversibility, hidden state and objectives set by observations.

## §6 Conclusion

- Claim: the problems are "equivalent". The call is for joint work on reward misspecification, safe exploration and observation ambiguity, through shared benchmarks, formalisms and evaluation.
- Quotes:
  - "By showing these problems are equivalent"
  - "shared benchmarks that test both RL and AI agents on the same sequential decision-making problems"
- For us: §6 says "equivalent", while §5 says "approximate equivalence". Our call to action can adopt their shared-benchmark proposal.

## §7 Acknowledgments and Appendix A

- Appendix A: agent definitions and successes (AI Scientist, Coscientist, SWE-agent, OpenHands, oncology agent). No safety tools.
- For us: nothing.

## Gaps this read exposed, and their status (2026-11-24)

1. Lee 2025: main text read in full (appendices not read) and added to the tool table. It learns irreversible states only by entering them, and a human then resets the agent; there is no guarantee.
2. Vasan 2024, Knox 2023, Tse 2025, Klissarov and Machado 2023: read in part and added to the tool table (notes and cells in 050, 063, 065).
3. Elelimy 2025b: read in part and added to the tool table. It rejects ergodicity for the real world, which supports S6. [1]'s phrase "learn an explicit mapping" does not match the paper, where the map is "some fixed partition of the histories".
4. The §3.6.2 sentence in the draft is fixed: Wachi is now cited as [1]'s §1 citation.
5. The conclusion is rescoped to guarantees, with counts computed from the tool table.
