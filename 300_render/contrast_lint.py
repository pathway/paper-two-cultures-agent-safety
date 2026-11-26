"""Find comparative claims in the draft and map each to settings and a coded property (D15).

Imperative shell around one port, `ask(prompt) -> str` (default adapter: Claude CLI, Haiku, subscription login).
A model reads each paragraph, because comparative claims do not have a fixed surface form; the build then checks
each mapped claim deterministically against the codes (100_analysis/contrasts.sentence_problems).
Results are cached by paragraph hash in contrast_lint.json, so the build makes no model call and is repeatable.
Usage: python3 contrast_lint.py        (lints paragraphs whose hash is not cached)
"""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "contrast_lint.json"
MODEL = "claude-haiku-4-5-20251001"

PROMPT = """You check a paper paragraph for comparative claims about agent settings.

Settings (id: phase, culture, description):
{settings}

Coded properties (id: question):
{properties}

A comparative claim says that something holds in some settings and not in others: RL agents versus LLM agents, training versus deployment, chatbots versus tool agents, one setting versus another. It is also comparative when a statement about one group of settings is offered as distinctive of that group (for example "in the LLM deployment settings there is no reward"): then the implied comparison group is the group it is distinguished from, and you must name it.

Also report similarity claims (something holds in both groups: "neither ... nor", "both", "too", "as ... is", "like"), claims that settings within one group vary, and general framing claims about the cultures or the meaning of "agent" that do not concern one property.

For each claim, return an object:
- "span": the claim's words copied exactly from the paragraph (one sentence or less);
- "a": the setting ids on one side; "b": the setting ids on the other side (use only ids from the list; "RL agents" in general means T-RL and D-RL; "LLM agents" or "LLM settings" in general means all LLM settings; "deployment" means the D- settings, "training" the T- settings);
- "relation": "differ" (holds in a, not in b), "differ_on" (a and b differ on whether it holds, without saying which side has it, e.g. "they differ on whether the environment resets"), "same" (holds in both a and b), "varies_within" (settings inside a differ; b is empty) or "general" (framing over many properties or about meaning; not about one property);
- "property": the id of the single coded property the claim is about, or null if none expresses it (always null for "general");
- "implicit": true if the comparison group was implied, not stated;
- "hedged": true if the sentence qualifies the claim (may, can, some, often, when episodic, partly), false if it states it outright.
A claim that names several properties is several claims: one object per property, each with the same span. A ranking or count over properties ("closest to", "differs on four properties") is not "general": report one claim per property it rests on, with property null if the sentence does not name them.
Do not report claims about a single cited paper, about Breiman's statistics, or about citation counts. Return only a JSON list; [] if there is none.

Paragraph:
<<<
{paragraph}
>>>"""


RELATIONS = ("differ", "differ_on", "same", "varies_within", "general")
PROMPT_VERSION = "4"     # part of the cache key: a changed prompt re-lints every paragraph


def paragraph_hash(text):
    return hashlib.sha256((PROMPT_VERSION + "\0" + text).encode()).hexdigest()[:16]


def prompt_for(paragraph, settings, properties):
    s = "\n".join(f"{x['id']}: {x['phase']}, {x['culture']}, {x['label']}; {x['posed_as']}" for x in settings)
    p = "\n".join(f"{x['id']}: {x['question']}" for x in properties)
    return PROMPT.format(settings=s, properties=p, paragraph=paragraph)


def parse(answer):
    """Model answer -> list of claims. The first JSON list in the answer is taken, so prose around it is ignored;
    no list at all is an error the caller records."""
    start = answer.find("[")
    if start < 0:
        raise ValueError("no JSON list in the answer")
    items, _ = json.JSONDecoder().raw_decode(answer[start:])
    if not isinstance(items, list):
        raise ValueError("not a list")
    return [claim for x in items if isinstance(x, dict) for claim in _claims(x)]


def _claims(x):
    """One raw item -> one claim per property it names (a list of properties is several claims)."""
    props = x.get("property") if isinstance(x.get("property"), list) else [x.get("property")]
    return [{"span": str(x.get("span") or ""), "a": list(x.get("a") or []), "b": list(x.get("b") or []),
             "property": prop, "relation": x.get("relation") if x.get("relation") in RELATIONS else "differ",
             "implicit": bool(x.get("implicit", False)), "hedged": bool(x.get("hedged", False))} for prop in props or [None]]


ADJUDICATE = """A cheap model read a paper paragraph and extracted the claim below; a deterministic check then failed it. Decide whether the failure comes from a wrong extraction (mapping_error) or from the paper's text (real).

Settings (id: phase, culture, description):
{settings}

Coded properties (id: question):
{properties}

Codes of the property involved, per setting (if any):
{codes}

Paragraph:
<<<
{paragraph}
>>>

Extracted claim: {claim}
Check result: {problem}

Rules. mapping_error: the paragraph does not say what the extraction says (wrong settings, wrong property, a similarity or framing statement read as a difference, a claim about a cited paper read as a claim about settings). Then give the corrected claim in the same schema (span, a, b, property, relation in differ|differ_on|same|varies_within|general, implicit, hedged). A sentence saying that groups differ on whether a property holds, without saying which side has the property, is relation differ_on; extracted as differ, it is a mapping_error, and a partly code needs no hedge under differ_on (D18). real: the paragraph does assert a difference or similarity between settings that the codes do not support, or a difference across phases attributed to culture. Return only JSON: {{"verdict": "mapping_error"|"real", "claim": <corrected claim, a list of claims, or null when the paragraph makes no comparative claim here>, "reason": "<one sentence>"}}."""


def span_key(span):
    """A span as compared with an override: surrounding space and trailing punctuation do not matter."""
    return span.strip().rstrip(".;,: ")


def effective(claim):
    """The claims the build checks: the adjudicated mapping (possibly none) when the adjudicator found a mapping
    error, else the claim itself."""
    adj = claim.get("adjudication") or {}
    return adj["claims"] if adj.get("verdict") == "mapping_error" else [claim]


def adjudicate(cache, failing, codes_for, ask, context=lambda: ("", ""), current=None, save=lambda cache: None):
    """Second pass, failing claims only: a stronger model decides mapping_error (with a corrected claim) or real.
    failing(claim) -> problem text or ''; codes_for(claim) -> text; current: paragraph hashes to read (None = all).
    Verdicts are cached on the claim, and the cache is saved after each one."""
    settings_text, properties_text = context()
    for h, entry in cache.items():
        if current is not None and h not in current:
            continue
        for c in entry.get("claims", []):
            problem = failing(c)
            if not problem or "adjudication" in c:
                continue
            prompt = ADJUDICATE.format(settings=settings_text, properties=properties_text, codes=codes_for(c),
                                       paragraph=entry["paragraph"], claim=json.dumps({k: c.get(k) for k in ("span", "a", "b", "property", "relation", "hedged")}),
                                       problem=problem)
            answer = ask(prompt)
            try:
                start = answer.find("{")
                adj, _ = json.JSONDecoder().raw_decode(answer[start:])
                found = adj.pop("claim", None)
                found = found if isinstance(found, list) else [found] if found else []
                for x in found:                      # an omitted hedge is inherited from the claim being corrected
                    if isinstance(x, dict) and "hedged" not in x:
                        x["hedged"] = c.get("hedged", False)
                adj["claims"] = parse(json.dumps(found))
            except (ValueError, json.JSONDecodeError, AttributeError) as e:
                adj = {"verdict": "error", "reason": str(e)}
            c["adjudication"] = adj
            save(cache)
            print("adjudicated", adj.get("verdict"), c["span"][:70])
    return cache


def sonnet_cli(prompt):
    """Adapter for the adjudication port: Claude CLI, Sonnet, subscription login."""
    run = subprocess.run(["env", "-u", "ANTHROPIC_API_KEY", "-u", "ANTHROPIC_AUTH_TOKEN", "claude", "-p", "--model", "sonnet"],
                         input=prompt, capture_output=True, text=True, timeout=600)
    return run.stdout


def claude_cli(prompt):
    """Adapter for the `ask` port: Claude CLI in print mode on the subscription login (API keys stripped)."""
    run = subprocess.run(["env", "-u", "ANTHROPIC_API_KEY", "-u", "ANTHROPIC_AUTH_TOKEN", "claude", "-p", "--model", MODEL],
                         input=prompt, capture_output=True, text=True, timeout=300)
    return run.stdout


def lint(paragraphs, settings, properties, cache, ask, save=lambda cache: None):
    """Lint each paragraph not yet cached; returns the updated cache {hash: {paragraph, claims} | {paragraph, error}}."""
    for para in paragraphs:
        h = paragraph_hash(para)
        if h in cache and "claims" in cache[h]:
            continue
        try:
            cache[h] = {"paragraph": para, "claims": parse(ask(prompt_for(para, settings, properties)))}
        except (ValueError, json.JSONDecodeError) as e:
            cache[h] = {"paragraph": para, "error": str(e)}
        save(cache)
        print(h, len(cache[h].get("claims", [])), "claims", cache[h].get("error", ""))
    return cache


def main():
    sys.path.insert(0, str(HERE))
    import build                                     # reuse the build's loader and draft expansion
    d = build.load()
    settings = list(csv.DictReader(open(ROOT / "060_settings/settings.csv", newline="")))
    properties = list(csv.DictReader(open(ROOT / "064_properties/properties.csv", newline="")))
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    save = lambda c: CACHE.write_text(json.dumps(c, indent=1, ensure_ascii=False))
    paragraphs = build.prose_paragraphs(d)
    cache = lint(paragraphs, settings, properties, cache, claude_cli, save)
    sys.path.insert(0, str(ROOT / "100_analysis"))
    import contrasts
    grid = contrasts.code_grid(d["codes"])
    failing = lambda c: "; ".join(contrasts.sentence_problems(c, grid, settings))
    codes_for = lambda c: "; ".join(f"{s['id']}={grid[(c['property'], s['id'])]}" for s in settings) if c.get("property") in {p["id"] for p in properties} else "(no property)"
    ctx = lambda: ("\n".join(f"{x['id']}: {x['phase']}, {x['culture']}, {x['label']}" for x in settings),
                   "\n".join(f"{x['id']}: {x['question']}" for x in properties))
    adjudicate(cache, failing, codes_for, sonnet_cli, ctx, current={paragraph_hash(p) for p in paragraphs}, save=save)


if __name__ == "__main__":
    main()
