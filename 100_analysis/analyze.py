"""Facts computed from the stage tables. Pure functions; I/O only in load() and main().

Reads 060, 062, 065, 070, 075, 078, 080. Writes facts.json, which 200_draft imports as {{fact:<id>}}, and sensitivity.md.
A count is printed as a number word; a share as a percentage; a share that rests on model-judged labels carries the marker [U] (decision D5).
"""
from collections import Counter, defaultdict
from pathlib import Path
import ast
import csv
import json
import math
import contrasts

ROOT = Path(__file__).resolve().parent.parent
WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
MCLEAN_CLASSES = {"misspecification", "irreversible-action-without-info", "insufficient-observation"}   # decision D8
UNAUDITED = " [U]"


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def number_word(n):
    return WORDS[n] if n < len(WORDS) else str(n)


def count_phrase(k, n):
    if k == n == 2:
        return "both"
    return f"all {number_word(n)}" if k == n else f"{number_word(k)} of {number_word(n)}"


def pct(k, n):
    return f"{round(100 * k / n)}%" if n else "n/a"


def share(k, n):
    """A share to one decimal. A nonzero count never prints as zero: 2 of 1117 is 0.2%, not 0%."""
    if not n:
        return "n/a"
    if k == 0:
        return "0%"
    text = f"{100 * k / n:.1f}%"
    return "<0.1%" if text == "0.0%" else text


def wilson(k, n, z=1.96):
    """95% Wilson interval for a share, as (low, high) in percent."""
    if not n:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (centre - half)), round(100 * (centre + half)))


def pct_ci(k, n):
    lo, hi = wilson(k, n)
    return f"{pct(k, n)} ({lo}–{hi})"


def join(items):
    items = list(items)
    if not items:
        return "none"
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def grid(cells):
    """[{primitive, setting, value}] -> {(primitive, setting): value}."""
    return {(c["primitive"], c["setting"]): c["value"] for c in cells}


def differing(g, a, b, order):
    """Primitives whose cell value differs between settings a and b, in table order."""
    return [p for p in order if g[(p, a)] != g[(p, b)]]


def settings_where(g, primitive, settings, prefix):
    """Settings whose cell for `primitive` starts with `prefix` (case-insensitive)."""
    return [s for s in settings if g[(primitive, s)].lower().startswith(prefix)]


def labels_of(labels, rater, dimension):
    """{incident: value} for one rater and dimension."""
    return {r["incident"]: r["value"] for r in labels if r["rater"] == rater and r["dimension"] == dimension}


def classes(value):
    """A failure-type label is stored as a Python list literal or a plain string -> list of class names."""
    try:
        v = ast.literal_eval(value)
        return [str(x) for x in v] if isinstance(v, (list, tuple)) else [str(v)]
    except (ValueError, SyntaxError):
        return [value] if value else []


def fits_mclean(value):
    return any(c in MCLEAN_CLASSES for c in classes(value))


def kappa(a, b):
    """Cohen's kappa between two {incident: category} maps over their common incidents."""
    common = sorted(set(a) & set(b))
    if not common:
        return float("nan")
    n = len(common)
    agree = sum(a[i] == b[i] for i in common) / n
    ca, cb = Counter(a[i] for i in common), Counter(b[i] for i in common)
    expected = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return 1.0 if expected == 1 else (agree - expected) / (1 - expected)


def tag_share(incidents, tag):
    k = sum(tag in [t.strip() for t in i["assumption_tags"].split(",")] for i in incidents)
    return k, len(incidents)


def coverage(incidents, labels, rater):
    """Shares of writable-in-advance verdicts and McLean-class fit for one rater, over the given incidents."""
    ids = {i["id"] for i in incidents}
    w = {k: v for k, v in labels_of(labels, rater, "writable_in_advance").items() if k in ids}
    f = {k: v for k, v in labels_of(labels, rater, "failure_type").items() if k in ids}
    n = len(w)
    return {
        "yes": sum(v == "yes" for v in w.values()), "partial": sum(v == "partial" for v in w.values()),
        "no": sum(v == "no" for v in w.values()), "n": n,
        "fit": sum(fits_mclean(v) for v in f.values()), "n_fit": len(f),
        "misspec": sum("misspecification" in classes(v) for v in f.values()),
        "injection": sum("injection/untrusted-input" in classes(v) for v in f.values()),
        "irreversible": sum("irreversible-action-without-info" in classes(v) for v in f.values()),
    }


def census_facts(m):
    a, b = m["cross_citation"]["A"], m["cross_citation"]["B"]
    com = m.get("community", {})
    out = {
        "corpus_a_n": str(m["sizes"]["A"]), "corpus_b_n": str(m["sizes"]["B"]), "bridge_n": number_word(m["sizes"]["bridge"]),
        "a_refs_to_a": f"{100 * a['frac_to_A']:.1f}%", "a_refs_to_b": f"{100 * a['frac_to_B']:.2f}%",
        "b_refs_to_b": f"{100 * b['frac_to_B']:.1f}%", "b_refs_to_a": f"{100 * b['frac_to_A']:.2f}%",
        "a_papers_citing_b": share(a["papers_citing_B"], a["papers"]), "b_papers_citing_a": share(b["papers_citing_A"], b["papers"]),
        "a_papers_citing_b_n": str(a["papers_citing_B"]), "b_papers_citing_a_n": str(b["papers_citing_A"]),
    }
    purity = com.get("purity") if isinstance(com, dict) else None
    out["louvain_purity"] = f"{purity:.2f}" if isinstance(purity, (int, float)) else "not computed"
    out["connected_n"], out["isolated_n"] = str(com.get("nodes_connected", "")), str(com.get("isolated_nodes", ""))
    return out


def facts(settings, primitives, cells, assumptions, incidents, labels, census, census_general=None,
          properties=(), codes=(), pairs=(), agreement=None):
    order = [p["id"] for p in primitives]
    label = {p["id"]: p["label"].lower() for p in primitives}
    S = [s["id"] for s in settings]
    g = grid(cells)
    deployment_llm = [s["id"] for s in settings if s["phase"] == "deployment" and s["group"] != "RL"]
    training_llm = [s["id"] for s in settings if s["phase"] == "training" and s["group"] != "RL"]
    names = lambda ps: join(label[p] for p in ps)
    deployed = [i for i in incidents if i["setting"] == "deployed-incident"]
    redteam = [i for i in incidents if i["setting"] == "red-team-on-product"]
    operator = labels_of(labels, "sonnet", "operator_type")
    deployer = [i for i in incidents if operator.get(i["id"]) == "deployer-operated"]
    cov_h, cov_s = coverage(incidents, labels, "haiku"), coverage(incidents, labels, "sonnet")
    injected = [i for i in incidents if "inject" in i["trigger"].lower()]
    all_three = [i for i in injected if {"A2", "C4", "D1"} <= {t.strip() for t in i["assumption_tags"].split(",")}]
    cov_dep = coverage(deployer, labels, "sonnet")
    w_h, w_s = labels_of(labels, "haiku", "writable_in_advance"), labels_of(labels, "sonnet", "writable_in_advance")
    f_h, f_s = labels_of(labels, "haiku", "failure_type"), labels_of(labels, "sonnet", "failure_type")
    d9b_h, d9b_s = labels_of(labels, "haiku", "D9b"), labels_of(labels, "haiku_b", "D9b")
    area10 = [i["id"] for i in incidents if all(c.startswith("D9b.10") for c in d9b_h.get(i["id"], "").split("; ") if c)
              and all(c.startswith("D9b.10") for c in d9b_s.get(i["id"], "").split("; ") if c) and d9b_h.get(i["id"])]
    out = {
        "settings_n": number_word(len(S)), "primitives_n": number_word(len(order)), "cells_n": str(len(cells)),
        "cells_quote_n": number_word(sum(c["evidence_type"] == "quote" for c in cells)),
        "cells_judgement_n": number_word(sum(c["evidence_type"] == "judgement" for c in cells)),
        "training_n": number_word(sum(s["phase"] == "training" for s in settings)),
        "deployment_n": number_word(sum(s["phase"] == "deployment" for s in settings)),
        "llm_deployment_n": number_word(len(deployment_llm)),
        "bandit_settings": join(settings_where(g, "transition", S, "none")),
        "bandit_settings_n": number_word(len(settings_where(g, "transition", S, "none"))),
        "drl_vs_dagentx": names(differing(g, "D-RL", "D-AGENT-X", order)),
        "drl_vs_dagentx_n": count_phrase(len(differing(g, "D-RL", "D-AGENT-X", order)), len(order)),
        "drl_vs_dchat": names(differing(g, "D-RL", "D-CHAT", order)),
        "dchat_vs_dagenta": names(differing(g, "D-CHAT", "D-AGENT-A", order)),
        "dchat_vs_dagenta_n": count_phrase(len(differing(g, "D-CHAT", "D-AGENT-A", order)), len(order)),
        "dagenta_vs_dagentx": names(differing(g, "D-AGENT-A", "D-AGENT-X", order)),
        "trl_vs_tchat": names(differing(g, "T-RL", "T-CHAT", order)),
        "trl_vs_tchat_n": count_phrase(len(differing(g, "T-RL", "T-CHAT", order)), len(order)),
        "trl_vs_tprm": names(differing(g, "T-RL", "T-PRM", order)),
        "trl_vs_tprm_n": count_phrase(len(differing(g, "T-RL", "T-PRM", order)), len(order)),
        "tchat_vs_trlvr": names(differing(g, "T-CHAT", "T-RLVR", order)),
        "tagent_vs_dagentx": names(differing(g, "T-AGENT", "D-AGENT-X", order)),
        "assumptions_n": number_word(len(assumptions)),
        "assumptions_rl_n": number_word(sum(a["owner"] == "RL" for a in assumptions)),
        "assumptions_llm_n": number_word(sum(a["owner"] == "LLM" for a in assumptions)),
        "assumptions_both_n": number_word(sum(a["owner"] == "Both" for a in assumptions)),
        "incidents_n": str(len(incidents)), "incidents_deployed_n": str(len(deployed)), "incidents_redteam_n": str(len(redteam)),
        "incidents_primary_n": str(sum(i["verification"] == "verified-primary" for i in incidents)),
        "deployer_n": str(len(deployer)) + UNAUDITED,
        "attacker_n": str(sum(operator.get(i["id"]) == "attacker-operated" for i in incidents)) + UNAUDITED,
        "writable_yes_h": pct_ci(cov_h["yes"], cov_h["n"]) + UNAUDITED, "writable_partial_h": pct_ci(cov_h["partial"], cov_h["n"]) + UNAUDITED,
        "writable_no_h": pct_ci(cov_h["no"], cov_h["n"]) + UNAUDITED,
        "writable_yes_s": pct_ci(cov_s["yes"], cov_s["n"]) + UNAUDITED, "writable_partial_s": pct_ci(cov_s["partial"], cov_s["n"]) + UNAUDITED,
        "writable_no_s": pct_ci(cov_s["no"], cov_s["n"]) + UNAUDITED,
        "writable_no_deployer": pct_ci(cov_dep["no"], cov_dep["n"]) + UNAUDITED,
        "writable_yes_deployer": pct_ci(cov_dep["yes"], cov_dep["n"]) + UNAUDITED,
        "writable_partial_deployer": pct_ci(cov_dep["partial"], cov_dep["n"]) + UNAUDITED,
        "injected_n": str(len(injected)), "injected_all_three": count_phrase(len(all_three), len(injected)), "writable_no_deployer_n": number_word(cov_dep["no"]) + UNAUDITED,
        "mclean_fit_h": pct_ci(cov_h["fit"], cov_h["n_fit"]) + UNAUDITED, "mclean_none_h": pct_ci(cov_h["n_fit"] - cov_h["fit"], cov_h["n_fit"]) + UNAUDITED,
        "mclean_fit_s": pct_ci(cov_s["fit"], cov_s["n_fit"]) + UNAUDITED, "mclean_none_s": pct_ci(cov_s["n_fit"] - cov_s["fit"], cov_s["n_fit"]) + UNAUDITED,
        "misspec_h": pct(cov_h["misspec"], cov_h["n_fit"]) + UNAUDITED, "misspec_s": pct(cov_s["misspec"], cov_s["n_fit"]) + UNAUDITED,
        "injection_h": pct(cov_h["injection"], cov_h["n_fit"]) + UNAUDITED, "injection_s": pct(cov_s["injection"], cov_s["n_fit"]) + UNAUDITED,
        "irreversible_h": pct(cov_h["irreversible"], cov_h["n_fit"]) + UNAUDITED,
        "kappa_writable": f"{kappa(w_h, w_s):.2f}" + UNAUDITED,
        "kappa_mclean_fit": f"{kappa({k: fits_mclean(v) for k, v in f_h.items()}, {k: fits_mclean(v) for k, v in f_s.items()}):.2f}" + UNAUDITED,
        "kappa_first_class": f"{kappa({k: (classes(v) or [''])[0] for k, v in f_h.items()}, {k: (classes(v) or [''])[0] for k, v in f_s.items()}):.2f}" + UNAUDITED,
        "area10_both": count_phrase(len(area10), len(incidents)) + UNAUDITED,
    }
    for a in assumptions:
        k, n = tag_share(incidents, a["id"])
        out[f"share_{a['id']}"] = pct(k, n) + UNAUDITED
    ranked = sorted(assumptions, key=lambda a: -tag_share(incidents, a["id"])[0])
    out["top_tags"] = join(f"{a['question'].lower()} ({pct(*tag_share(incidents, a['id']))})" for a in ranked[:3]) + UNAUDITED
    out.update(census_facts(census))
    if census_general:
        out.update({f"gen_{k}": v for k, v in census_facts(census_general).items()})
    if codes:
        out.update(contrast_facts(settings, properties, codes, pairs, agreement))
    return out


def revised_codes(codes):
    """Number of codes whose value a review round set, against the raters' or the adjudicator's value (column by)."""
    return sum(c.get("by", "").startswith("gate round") for c in codes)


def contrast_facts(settings, properties, codes, pairs, agreement):
    """Matched-contrast facts (D15): which properties move with culture (within a phase) and which with phase."""
    grid = contrasts.code_grid(codes)
    att = {p["id"]: contrasts.attribution(grid, p["id"], pairs, settings) for p in properties}
    label = {p["id"]: p["phrase"] for p in properties}
    pick = lambda f: [p["id"] for p in properties if f(att[p["id"]])]
    both_all = pick(lambda a: a["culture_training"] == "all" and a["culture_deployment"] == "all")
    deploy_only_all = pick(lambda a: a["culture_deployment"] == "all" and a["culture_training"] != "all")
    phase_only = pick(lambda a: a["label"] == "phase")
    # D17: process supervision against RL training, where both bandit settings (T-CHAT, T-RLVR) differ
    prm_like_rl = contrasts.shared_against(grid, [p["id"] for p in properties], "T-PRM", "T-RL", ["T-CHAT", "T-RLVR"])
    out = {
        "properties_n": number_word(len(properties)), "codes_n": str(len(codes)), "codes_revised_n": number_word(revised_codes(codes)),
        "culture_all_both_n": number_word(len(both_all)), "culture_all_both": join(label[i] for i in both_all),
        "culture_all_deploy_n": number_word(len(deploy_only_all)), "culture_all_deploy": join(label[i] for i in deploy_only_all),
        "phase_only_n": number_word(len(phase_only)), "phase_only": join(label[i] for i in phase_only),
        "prm_like_rl_n": number_word(len(prm_like_rl)), "prm_like_rl": join(label[i] for i in prm_like_rl),
    }
    if agreement:
        out.update({"coding_agreement": agreement["raw_agreement"], "coding_kappa": f"{agreement['kappa']:.2f}"})
    return out


def sensitivity(inputs):
    """{scenario: {fact: (baseline, value)}}: facts that change when the incident set or the rater changes."""
    base = facts(**inputs)
    scenarios = {
        "deployed incidents only": {"incidents": [i for i in inputs["incidents"] if i["setting"] == "deployed-incident"]},
        "red-team incidents only": {"incidents": [i for i in inputs["incidents"] if i["setting"] == "red-team-on-product"]},
        "primary-source incidents only": {"incidents": [i for i in inputs["incidents"] if i["verification"] == "verified-primary"]},
    }
    out = {}
    for name, change in scenarios.items():
        new = facts(**{**inputs, **change})
        out[name] = {k: (base[k], v) for k, v in new.items() if v != base[k]}
    return out


def sensitivity_report(changes):
    lines = ["# Sensitivity of the computed facts", "",
             "Generated by `100_analysis/analyze.py`. Each line restricts the incident set.",
             "A fact listed here changes under that scenario, so the sentence that prints it rests on the rows left out.", ""]
    for name, diff in changes.items():
        shown = "; ".join(f"{k}: {a} -> {b}" for k, (a, b) in diff.items()) or "no fact changes"
        lines.append(f"- **{name}**: {shown}")
    return "\n".join(lines) + "\n"


def load():
    return {"settings": read_csv(ROOT / "060_settings/settings.csv"), "primitives": read_csv(ROOT / "062_primitives/primitives.csv"),
            "cells": read_csv(ROOT / "065_primitive_cells/cells.csv"), "assumptions": read_csv(ROOT / "070_assumptions/assumptions.csv"),
            "incidents": read_csv(ROOT / "075_incidents/incidents.csv"), "labels": read_csv(ROOT / "078_incident_labels/labels.csv"),
            "census": json.loads((ROOT / "080_census/metrics.json").read_text()),
            "census_general": json.loads((ROOT / "080_census/general/metrics.json").read_text())
            if (ROOT / "080_census/general/metrics.json").exists() else None,
            "properties": read_csv(ROOT / "064_properties/properties.csv"), "codes": read_csv(ROOT / "066_property_codes/codes.csv"),
            "pairs": read_csv(ROOT / "063_contrasts/pairs.csv"),
            "agreement": json.loads((ROOT / "066_property_codes/agreement.json").read_text())}


def main():
    inputs = load()
    out = facts(**inputs)
    here = Path(__file__).parent
    (here / "facts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    (here / "sensitivity.md").write_text(sensitivity_report(sensitivity(inputs)))
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=1, ensure_ascii=False))
