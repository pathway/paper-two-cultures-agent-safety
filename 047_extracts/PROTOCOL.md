# Extraction protocol (forward step: 045_fulltext -> 047_extracts)

`scan.py` reads each full text and proposes passages under the topics below. Every passage must be verbatim; the scanner rejects any passage it cannot locate in the full text. Proposals go to `<key>/candidates.csv` (generated). A curator copies the useful ones to `<key>/extracts.csv`, which later stages cite by id.

The topics are neutral: they ask what the source says about each primitive of the decision problem, not whether it supports our argument. One topic per RL primitive, then the context around them.

| Topic | Extract the passage that states… |
|---|---|
| reward | what the reward (or cost, preference, verifier score, process score) is, who or what produces it, when it arrives, whether it is a scalar, and whether it exists after training |
| policy | what the policy is (a learned mapping, a frozen model, a model inside a scaffold), what varies at deployment, and whether it updates while acting |
| action | what one action is (a token, a whole completion, a reasoning step, a tool call), its space, and whether it has side effects outside the text |
| observation | what the agent observes, whether observations can contain instructions, and who authors them |
| state | what the state is, whether it is Markov, whether it is fully observed, and what is hidden |
| transition | what the dynamics are, whether they are known, deterministic, stationary, or controlled by third parties |
| episode | horizon, termination, resets, irreversibility, what persists after an episode |
| value | whether a value function, critic or return is defined or used, and what replaces it |
| objective | where the task objective or specification comes from, who writes it, and whether it can change during a run |
| principal | whose preferences the objective encodes, and how many parties (vendor, deployer, user, third party) |
| oversight | monitors, approval gates, traces, logs, and whether the agent models them |
| failure | what counts as failure or harm, what gets hacked or gamed, and reported incidents |
| claim | the main claim or contribution of the source |
| setting | the formal problem as posed: MDP, POMDP, bandit, tree, with what given and unknown |
| limitation | each limitation the authors state |
| llm | anything said about language models, chatbots or LLM agents in RL terms |
