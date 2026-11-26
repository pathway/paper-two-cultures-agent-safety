---
key: sutton2018
read: partial
read_detail: Chapter 1 (§1.1–1.3), Chapter 3 (§3.1–3.5), Chapter 17 (§17.3–17.4) read; the rest of the book not read for this paper
read_on: 2026-11-25
---

# Sutton & Barto 2018: the RL reader's definitions of the primitives

Source: R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018. Full text: `045_fulltext/sutton2018.txt` (548 pages).
Role in this paper: the target vocabulary. The paper asks what each of these words denotes in LLM chatbots and LLM tool agents; the book fixes what an RL reader takes them to mean.

| Primitive | Where | Extract |
|---|---|---|
| agent / environment | §3.1 | e1 |
| reward | §3.1, §3.2 (reward hypothesis) | e2, e8, e9, e10, e16 |
| action | §3.1 | e3, e7 |
| observation / state | §3.1 | e3, e5 |
| transition | §3.1 | e4 |
| episode, time step | §3.1, §3.3 | e6, e11, e12 |
| policy | §1.3, §3.5 | e13, e14, e15 |
| value | §3.5 | e17 |

Key points
- The reward is a signal "passing from the environment to the agent" and is "a simple number" at each step (e8). The reward hypothesis makes goals equal to maximising its expected cumulative sum (e9).
- The reward is the designer's channel for "what you want achieved, not how" (e10), and the designer must make it "truly indicate what we want accomplished" (e16).
- A policy is a mapping from states to action probabilities (e13), and RL methods are defined by how they change it from experience (e14).
- Time steps are abstract: "arbitrary successive stages of decision making and acting" (e6); actions can be high-level decisions (e7). This is the flexibility that McLean et al. use to write an LLM agent as a POMDP.
- Episodes end in a terminal state "followed by a reset" and begin "independently of how the previous one ended" (e11, e12).

Verified quotes
- "The learner and decision maker is called the agent."
- "passing from the environment to the agent"
- "a received scalar signal (called reward)"
- "what you want achieved, not how you want it achieved"
- "Formally, a policy is a mapping from states to probabilities of selecting each possible action."
- "followed by a reset to a standard starting state"
- "the next episode begins independently of how the previous one ended"
- "arbitrary successive stages of decision making and acting"
