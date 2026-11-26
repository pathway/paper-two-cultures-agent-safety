"""Matched contrasts over coded properties. Pure functions; no I/O.

A difference is attributed to an axis only between settings that differ on that axis alone (declared pairs, 063).
Culture pairs hold phase fixed; phase pairs hold culture fixed. This is what stops a training-vs-deployment
difference being reported as an RL-vs-LLM difference (decision D15, research note 20).
"""
from collections import defaultdict

PHASES = ("training", "deployment")
CULTURES = ("RL", "LLM")


def code_grid(codes):
    """[{property, setting, code}] -> {(property, setting): code}."""
    return {(c["property"], c["setting"]): c["code"] for c in codes}


def pair_problems(pairs, settings):
    """A declared pair must name known settings and differ on its axis only, as far as phase and culture go."""
    s = {x["id"]: x for x in settings}
    out = []
    for p in pairs:
        a, b = s.get(p["a"]), s.get(p["b"])
        if not a or not b:
            out.append(f"pair {p['id']}: unknown setting")
            continue
        same_phase, same_culture = a["phase"] == b["phase"], a["culture"] == b["culture"]
        if p["axis"] == "culture" and not (same_phase and not same_culture):
            out.append(f"pair {p['id']}: a culture pair must hold phase fixed and differ in culture")
        if p["axis"] == "phase" and not (same_culture and not same_phase):
            out.append(f"pair {p['id']}: a phase pair must hold culture fixed and differ in phase")
        if p["axis"] in ("tools", "human") and not (same_phase and same_culture):
            out.append(f"pair {p['id']}: a {p['axis']} pair must hold phase and culture fixed")
    return out


def attribution(grid, prop, pairs, settings):
    """How a property moves: per phase, whether the culture pairs differ (all / some / none); per culture,
    whether the phase pairs differ; and a label: culture, phase, culture and phase, or neither."""
    phase_of = {s["id"]: s["phase"] for s in settings}
    culture_of = {s["id"]: s["culture"] for s in settings}
    differs = lambda p: grid[(prop, p["a"])] != grid[(prop, p["b"])]
    out = {}
    for ph in PHASES:
        cp = [p for p in pairs if p["axis"] == "culture" and phase_of[p["a"]] == ph]
        n = sum(differs(p) for p in cp)
        out[f"culture_{ph}"] = "none" if n == 0 else ("all" if n == len(cp) else "some")
    for cu in CULTURES:
        pp = [p for p in pairs if p["axis"] == "phase" and culture_of[p["a"]] == cu]
        out[f"phase_{cu}"] = "yes" if any(differs(p) for p in pp) else "no"
    by_culture = any(out[f"culture_{ph}"] != "none" for ph in PHASES)
    by_phase = any(out[f"phase_{cu}"] == "yes" for cu in CULTURES)
    out["label"] = {(True, True): "culture and phase", (True, False): "culture", (False, True): "phase", (False, False): "neither"}[(by_culture, by_phase)]
    return out


def contrast_problems(claims, grid, pairs, settings, properties):
    """095 claims of kind contrast: the stated axis, phase or culture, and extent must be what the codes give."""
    known = {p["id"] for p in properties}
    out = []
    for c in claims:
        if c["kind"] != "contrast":
            continue
        if c["property"] not in known:
            out.append(f"contrast claim {c['id']}: unknown property {c['property']!r}")
            continue
        a = attribution(grid, c["property"], pairs, settings)
        if c["axis"] == "culture":
            got = a.get(f"culture_{c['phase']}")
            if got is None or got == "none" or (c["extent"] == "all" and got != "all"):
                out.append(f"contrast claim {c['id']}: says {c['property']} differs by culture in {c['phase']} ({c['extent']}), codes give {got}")
        elif c["axis"] == "phase":
            if a.get(f"phase_{c['culture']}") != "yes":
                out.append(f"contrast claim {c['id']}: says {c['property']} differs by phase within {c['culture']}, codes do not")
            if c.get("extent") == "only" and a["label"] != "phase":
                out.append(f"contrast claim {c['id']}: says {c['property']} differs by phase only, codes give {a['label']}")
        else:
            out.append(f"contrast claim {c['id']}: axis must be culture or phase")
    return out


def sentence_problems(claim, grid, settings):
    """A comparative claim found in prose (by contrast_lint): groups a and b of settings, and a property.
    Fails on a phase confound (cultures and phases both differ, unmatched), on codes that do not separate the groups
    (within a shared phase, or within a shared culture across phases), and on a 'partly' code the sentence does not hedge."""
    phase_of = {s["id"]: s["phase"] for s in settings}
    culture_of = {s["id"]: s["culture"] for s in settings}
    A, B, prop = claim["a"], claim["b"], claim.get("property")
    relation = claim.get("relation", "differ")
    if relation in ("general", "varies_within"):
        return []                                   # listed in out/contrasts.md for the review lens, not checked here
    unknown = [x for x in A + B if x not in phase_of]
    if unknown:
        return [f"unknown settings {unknown}"]
    if relation == "same":
        if not prop:
            return ["unregistered similarity: no property in 064 expresses it; add one or reword"]
        codes = {grid[(prop, x)] for x in A + B}
        return [] if len(codes) == 1 else [f"{prop}: stated as the same, but the codes are {sorted(codes)}, so it is not the same"]
    if not prop:
        return ["unregistered contrast: no property in 064 expresses it; add one or reword"]
    out = []
    phases_a, phases_b = {phase_of[x] for x in A}, {phase_of[x] for x in B}
    cultures_a, cultures_b = {culture_of[x] for x in A}, {culture_of[x] for x in B}
    if cultures_a != cultures_b and not (phases_a & phases_b):
        out.append(f"phase confound: compares {sorted(cultures_a)} in {sorted(phases_a)} with {sorted(cultures_b)} in {sorted(phases_b)}")
    for ph in sorted(phases_a & phases_b):
        ca = {grid[(prop, x)] for x in A if phase_of[x] == ph}
        cb = {grid[(prop, x)] for x in B if phase_of[x] == ph}
        if ca & cb:
            out.append(f"{prop} in {ph}: the groups share code(s) {sorted(ca & cb)}, so the stated difference does not hold")
    for ph in sorted((phases_a | phases_b) - (phases_a & phases_b)):
        if cultures_a != cultures_b:
            out.append(f"{prop}: the {ph} side has no same-phase comparison group")
    if not (phases_a & phases_b):
        for c in sorted(cultures_a & cultures_b):
            ca = {grid[(prop, x)] for x in A if culture_of[x] == c}
            cb = {grid[(prop, x)] for x in B if culture_of[x] == c}
            if ca & cb:
                out.append(f"{prop} within {c}: the groups share code(s) {sorted(ca & cb)}, so the stated phase difference does not hold")
    partly = [x for x in A + B if grid[(prop, x)] == "partly"]
    if relation == "differ" and partly and not claim.get("hedged"):   # differ_on states no direction, so no hedge is due
        out.append(f"{prop} is partly in {partly}: the sentence states it without qualification")
    return out


def summarise(grid, prop, ids):
    """Codes of a property over settings, compact: 'no' if uniform, else 'yes: A, B; no: C'."""
    by = defaultdict(list)
    for s in ids:
        by[grid[(prop, s)]].append(s)
    if len(by) == 1:
        return next(iter(by))
    return "; ".join(f"{k}: {', '.join(v)}" for k, v in sorted(by.items()))


def shared_against(grid, props, setting, reference, rivals):
    """Properties on which `setting` has the code of `reference` and every rival has another code."""
    return [p for p in props if grid[(p, setting)] == grid[(p, reference)]
            and all(grid[(p, r)] != grid[(p, reference)] for r in rivals)]
