---
key: mclean2026
read: full
read_detail: full text from a local PDF copy; §1, §3.6, §4, §5, §6 and references re-checked
read_on: 2026-11-24
---

# McLean et al. 2026: which paper it cites for each tool

Source: [1] McLean et al., "AI Agent Safety is a Reinforcement Learning Problem", AIWILD @ ICML 2026. https://openreview.net/forum?id=wvga9chmb6
Read: full text (local PDF copy from an earlier session), sections 1, 3.6, 4, 5, 6 and the reference list checked on 2026-11-24.

| Tool or claim in [1] | Where in [1] | Paper cited |
|---|---|---|
| Constraining agent behaviour; CMDP | §1, §3.6.2, §4, §5 | Altman 1999; Satija, Amortila, Pineau 2020 |
| Diagnosing reward misspecification / reward function alignment | §1, §5 | Muslimani et al. 2025 (also Vasan et al. 2024; Knox et al. 2023) |
| Ensuring safe exploration | §1 | Wachi et al. 2023 |
| Safe sequential decision-making under uncertainty | §3 | Mohammedalamen et al. 2025 ("Learning to be cautious"); Mohammedalamen and Bowling 2025 (Mon-MDPs) |
| Belief-state planning for observation ambiguity | §3.6.3 | Kaelbling, Littman, Cassandra 1998 |
| Shielding ("safety shield", "exact runtime shielding") | §3.6.2, §5 | **No citation** |
| Reward misspecification (more) | §3.5 | Vasan et al. 2024; Knox et al. 2023 |
| Exploration | §3.5; options in §4 | Tse et al. 2025; Klissarov and Machado 2023 (also Jinnai 2020 in §4) |
| History-to-state map against the finite context window | §4 | Elelimy et al. 2025b |
| Reward hacking theorem | §3.6.1 | Skalse et al. 2022 (a theorem, not a tool) |
| Irreversible states | §3.6.2 | Lee 2025 |

Key points
- [1] does not cite CPO (Achiam 2017), Moldovan–Abbeel 2012 or Safety Gym (Ray 2019). Our earlier tables used these; that was our error.
- §3.6.2 presents safe exploration and CMDPs as what is "missing" for irreversible actions such as `rm -rf /`.
- §5 concedes: classical algorithms "rely on tabular representations, exact runtime shielding, or known transition matrices" and "cannot be mapped one-to-one onto LLM backbones".

Verified quotes (checked against the source text, 2026-11-24)
- "diagnose and address" (Abstract)
- "tabular representations, exact runtime shielding, or known transition matrices" (§5)
- "cannot be mapped one-to-one onto LLM backbones" (§5)
- "a significant scaling gap exists" (§5)
- "a profound opportunity for the community to scale foundational RL principles up to high-dimensional, semantic domains" (§5)
- "complementary framework for structural safety" (§5)
- "provides a diagnostic lens" (§4)
- "The former is what is missing from deployed AI Agents" (§3.6.2; "the former" is a safety shield at inference time)
- "irreversible states" (§3.6.2)
- "to mask the deletion" (§3.6.1)
- "the user's intents, safety constraints" (§3.5)
- "the transition function is rarely known" (§3.4)
- "This is a lossy process" (§3.5)
- "training (updating the policy) to deployment (freezing the policy)" (§3.5)
- "operates at inference time over the action space" (§3.6.2)
- "it is impossible to return to a safe or functional state" (§3.6.2)
- "The only way that a user can interact with the AI agent during deployment is through the initial prompt" (§3.6.1)
- "the individual AI agent that is built on top of a LLM" (§2)
- "does not inherently solve the foundational challenge of specifying a flawless objective function" (§5)
- "has not yet followed" (§3.5)
- "games or simulations" (§3.6.2)
- "ensuring safe exploration" (§1)
- "provides a diagnostic lens for discussing and solving these reward specification problems" (§4)
- "Once this training step is completed the PRM is no longer used" (§4)

Incidents in [1]: four are listed in §1 (database deletion, Nolan 2025; cryptocurrency mining, Wang et al. 2026; data leak, Down 2026; inbox deletion, Martindale 2026). Two are worked through: Replit (§3.6.1, the database deletion) and Terraform (§3.6.3, Grigorev 2025), so five distinct incidents. §3.6.2 uses a hypothetical (`rm -rf /`).
Checked against the primary reports (045_fulltext, 2026-11-24): [1] date the Terraform incident to February 2025; the post dates it to 26 February 2026. Both worked incidents were restored afterwards (a platform rollback; a vendor snapshot after about 24 hours); [1] do not say so. The Register reports fake data made to cover "bugs and issues", not to mask the deletion.
