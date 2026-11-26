"""Build the PDF from the stage folders. Imperative shell: reads files, calls pandoc and pdflatex.

Pipeline: checks (incl. quotes against 045_fulltext and 047_extracts) -> out/backcheck.md -> 100_analysis facts
-> expand {{directives}} in 200_draft -> pandoc (--natbib) -> template -> pdflatex.
Usage: python3 build.py
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

import yaml

import backcheck
import checks
import claims
import render

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "100_analysis"))
import analyze  # noqa: E402
import contrasts  # noqa: E402

RUNNING_TITLE = "The Two Cultures of Agents"
COUNTED_NOUNS = ["settings", "setting", "primitives", "primitive", "cells", "incidents", "incident", "works", "papers",
                 "assumptions", "references", "rows", "sources"]
TARGETS = ["sutton2018", "mclean2026", "breiman2001"]          # sources whose full text and extracts the build requires


def read_csv(rel):
    with open(ROOT / rel, newline="") as f:
        return list(csv.DictReader(f))


def pandoc(markdown):
    out = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--natbib", "--wrap=preserve",
                          "--shift-heading-level-by=-1"], input=markdown, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def pandoc_many(cells):
    """Convert many short markdown strings in one pandoc call; empty strings stay empty."""
    sep = "\n\nZZCELLSEPZZ\n\n"
    filled = [c for c in cells if c.strip()]
    converted = iter(c.strip() for c in pandoc(sep.join(filled)).split("ZZCELLSEPZZ")) if filled else iter(())
    return [next(converted) if c.strip() else "" for c in cells]


def load():
    d = {
        "refs": yaml.safe_load((ROOT / "040_biblio/refs.yaml").read_text()),
        "notes": {p.stem: p.read_text() for p in list((ROOT / "050_biblio_notes").glob("*.md")) + list((ROOT / "010_target").glob("*.md"))
                  if not p.stem.endswith("_sections")},
        "existence": read_csv("040_biblio/existence.csv"),
        "manifest": read_csv("045_fulltext/manifest.csv"),
        "snapshots": read_csv("045_fulltext/web_manifest.csv"),
        "decisions": read_csv("005_decisions/decisions.csv"),
        "claims": read_csv("095_claims/claims.csv"),
        "settings": read_csv("060_settings/settings.csv"),
        "primitives": read_csv("062_primitives/primitives.csv"),
        "cells": read_csv("065_primitive_cells/cells.csv"),
        "assumptions": read_csv("070_assumptions/assumptions.csv"),
        "incidents": read_csv("075_incidents/incidents.csv"),
        "labels": read_csv("078_incident_labels/labels.csv"),
        "cultures": read_csv("085_breiman/cultures.csv"),
        "census": json.loads((ROOT / "080_census/metrics.json").read_text()),
        "census_general": json.loads((ROOT / "080_census/general/metrics.json").read_text())
        if (ROOT / "080_census/general/metrics.json").exists() else None,
        "properties": read_csv("064_properties/properties.csv"),
        "codes": read_csv("066_property_codes/codes.csv"),
        "pairs": read_csv("063_contrasts/pairs.csv"),
        "lint": json.loads((HERE / "contrast_lint.json").read_text()) if (HERE / "contrast_lint.json").exists() else {},
        "overrides": read_csv("300_render/contrast_overrides.csv"),
        "related": (ROOT / "090_related/related.md").read_text().split("-->", 1)[-1].strip(),
        "draft": (ROOT / "200_draft/draft.md").read_text(),
    }
    d["fulltexts"] = {m["key"]: (ROOT / "045_fulltext" / m["file"]).read_text(errors="replace") for m in d["manifest"]
                      if (ROOT / "045_fulltext" / m["file"]).exists()}
    d["extracts"] = {p.parent.name: read_csv(p.relative_to(ROOT)) for p in sorted((ROOT / "047_extracts").glob("*/extracts.csv"))}
    d["tex_sources"] = {p.name: "\n".join(f.read_text(errors="replace") for f in sorted(p.glob("*.tex")))
                        for p in sorted((ROOT / "045_fulltext/tex").glob("*")) if p.is_dir()}
    d["formula_images"] = {(p.parent.name, p.stem) for p in (ROOT / "047_extracts").glob("*/*.png")}
    return d


def quote_uses(d):
    """(evidence, listed, prose): quotes whose source is known from where they stand, note quotes, and quotes in running text."""
    Use, quotes = backcheck.Use, checks.QUOTE.findall
    evidence = [Use(c["evidence_source"], f"cell {c['primitive']} {c['setting']}", q) for c in d["cells"] if c["evidence_source"] for q in quotes(c["reason"])]
    evidence += [Use(c["evidence_source"], f"culture {c['id']}", q) for c in d["cultures"] if c["evidence_source"] for q in quotes(c["text"])]
    listed = [Use(k, f"note {k}", q) for k, note in d["notes"].items() for q in checks.verified_quotes(note)]
    indexes = {k: backcheck.build_index(t) for k, t in d["fulltexts"].items()}
    texts = {"draft": d["draft"], "related work": d["related"]}
    texts.update({f"{k} row {i}": " ".join(row.values()) for k in ("settings", "primitives", "assumptions")
                  for i, row in enumerate(d[k], 2)})
    texts.update({f"cell {c['primitive']} {c['setting']}": c["reason"] for c in d["cells"] if not c["evidence_source"]})
    prose = []
    for where, text in texts.items():
        cited_first = {k: indexes[k] for k in render.cite_keys(text) if k in indexes}
        prose += [Use(backcheck.attribute(q, {**cited_first, **indexes}), where, q) for q in quotes(checks.normalise(text))]
    return evidence, listed, prose


def cited_evidence(d):
    out = {f"cell {c['primitive']} {c['setting']}": checks.split_list(c["evidence"]) for c in d["cells"]}
    out.update({f"culture {c['id']}": checks.split_list(c["evidence"]) for c in d["cultures"]})
    return out


def census_stale(d):
    """080: the metrics snapshot and corpora must match SHA256SUMS."""
    out = []
    for sums in (ROOT / "080_census/SHA256SUMS", ROOT / "080_census/general/SHA256SUMS"):
        for line in sums.read_text().splitlines():
            want, name = line.split()
            have = hashlib.sha256((sums.parent / name).read_bytes()).hexdigest()
            if want != have:
                out.append(f"{sums.parent.relative_to(ROOT)}/{name}: hash differs from SHA256SUMS; the census snapshot changed")
    return out


def prose_paragraphs(d):
    """Paragraphs of the draft and related work as printed (facts and claims expanded, tables left out): the
    unit the contrast linter reads."""
    facts = analyze.facts(**analyze.load())
    phrases = {c["id"]: c["text"] for c in d["claims"] if c["kind"] in ("set", "scope", "contrast")}
    resolve = {"fact": lambda k: facts.get(k, phrases.get(k, k)), "table": lambda k: "", "include": lambda k: d[k], "appendix": lambda k: ""}
    text = render.expand(d["draft"], resolve)
    return [p.strip() for p in text.split("\n\n") if p.strip() and not p.lstrip().startswith(("#", "```"))]


def code_problems(d):
    """066 complete and valid; 063 pairs minimal; 095 contrast claims match the codes."""
    S = [s["id"] for s in d["settings"]]
    have = {(c["property"], c["setting"]): c["code"] for c in d["codes"]}
    out = [f"code {p['id']} {s}: missing" for p in d["properties"] for s in S if (p["id"], s) not in have]
    out += [f"code {k}: bad value {v!r}" for k, v in have.items() if v not in ("yes", "no", "partly")]
    out += contrasts.pair_problems(d["pairs"], d["settings"])
    out += contrasts.contrast_problems(d["claims"], contrasts.code_grid(d["codes"]), d["pairs"], d["settings"], d["properties"])
    return out


def lint_problems(d):
    """Every printed paragraph must have been read by contrast_lint.py, and every comparative claim it found must be
    a matched contrast that the codes support, unless an override with a decision id covers its span."""
    from contrast_lint import paragraph_hash, effective, span_key
    grid = contrasts.code_grid(d["codes"])
    waived = {span_key(o["span"]) for o in d["overrides"] if o["decision"].strip()}
    out = []
    for para in prose_paragraphs(d):
        entry = d["lint"].get(paragraph_hash(para))
        if entry is None:
            out.append(f"paragraph not linted (run 300_render/contrast_lint.py): {para[:80]!r}")
            continue
        if "error" in entry:
            out.append(f"paragraph lint failed ({entry['error']}); rerun contrast_lint.py: {para[:80]!r}")
            continue
        for raw in entry["claims"]:
            for c in effective(raw):
                if span_key(c["span"]) in waived or span_key(raw["span"]) in waived:
                    continue
                problems = contrasts.sentence_problems(c, grid, d["settings"])
                if problems and "adjudication" not in raw:
                    out.append(f"contrast \"{c['span'][:90]}\": failing claim not adjudicated; rerun contrast_lint.py")
                out += [f"contrast \"{c['span'][:90]}\": {p} (adjudicated {raw.get('adjudication', {}).get('verdict', '-')})" for p in problems]
    return out


def contrast_report(d):
    """Markdown list of every claim the linter found, its relation, property and check result: the review lens reads it."""
    from contrast_lint import paragraph_hash, effective
    grid = contrasts.code_grid(d["codes"])
    lines = ["# Comparative claims found by contrast_lint.py", "", "relation | property | a | b | result | span", "", ]
    for para in prose_paragraphs(d):
        for c in (c for raw in d["lint"].get(paragraph_hash(para), {}).get("claims", []) for c in effective(raw)):
            res = contrasts.sentence_problems(c, grid, d["settings"])
            lines.append(f"- {c.get('relation', 'differ')} | {c.get('property')} | {', '.join(c['a'])} | {', '.join(c['b'])} | "
                         f"{'; '.join(res) or ('not checked (review lens)' if c.get('relation') in ('general', 'varies_within') else 'ok')} | {c['span']}")
    return "\n".join(lines) + "\n"


def run_checks(d):
    texts = [d["draft"], d["related"]] + [json.dumps(d[k], ensure_ascii=False) for k in ("settings", "primitives", "cells", "assumptions", "cultures")]
    cited = set().union(*(render.cite_keys(t) for t in texts))
    problems = (checks.missing_keys(texts, d["refs"]) + checks.existence_problems(cited, d["existence"])
                + checks.note_problems(TARGETS, d["notes"])
                + checks.settings_problems(d["settings"], d["decisions"])
                + checks.primitive_problems(d["primitives"], d["extracts"].get("sutton2018", []))
                + checks.cell_problems(d["primitives"], d["settings"], d["cells"])
                + checks.assumption_problems(d["assumptions"], d["refs"], d["primitives"])
                + checks.incident_problems(d["incidents"], d["assumptions"], d["snapshots"])
                + checks.label_problems(d["incidents"], d["labels"])
                + checks.culture_problems(d["cultures"], d["extracts"].get("breiman2001", []))
                + claims.stale(d["claims"], lambda path: (ROOT / path).read_text())
                + checks.typed_count_problems(d["draft"] + d["related"], COUNTED_NOUNS)
                + checks.draft_problems(d["draft"]) + census_stale(d) + code_problems(d) + lint_problems(d))
    evidence, listed, prose = quote_uses(d)
    problems += [f"{u.where}: quote not in any stored full text: \"{u.phrase}\"" for u in prose if not u.key]
    indexes = {k: backcheck.build_index(t) for k, t in d["fulltexts"].items()}
    paragraphs = {f"draft paragraph {i}": checks.normalise(p) for i, p in enumerate(d["draft"].split("\n\n"), 1)}
    paragraphs["related work"] = checks.normalise(d["related"])
    paragraphs.update({f"cell {c['primitive']} {c['setting']}": checks.normalise(c["reason"]) for c in d["cells"] if not c["evidence_source"]})
    problems += backcheck.misattributed_quotes(paragraphs, indexes, render.CITE_KEY)
    extract_uses = [backcheck.Use(k, f"extract {k} {e['id']}", e["text"]) for k, rows in d["extracts"].items() for e in rows]
    files = {(m["key"], kind): ROOT / "045_fulltext" / (f"pdf/{m['key']}.pdf" if kind == "pdf" else m["file"])
             for m in d["manifest"] for kind in ("pdf", "txt")}
    hashes = {k: hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None for k, p in files.items()}
    problems += (backcheck.stale_files(d["manifest"], hashes)
                 + [f"{k}: no full text in 045_fulltext" for k in TARGETS if k not in d["fulltexts"]]
                 + [f"{k}: no extracts in 047_extracts" for k in TARGETS if not d["extracts"].get(k)]
                 + backcheck.missing_in_fulltext(extract_uses + evidence + listed, d["fulltexts"])
                 + backcheck.not_covered_by_extracts(evidence, d["extracts"], cited_evidence(d))
                 + backcheck.formula_problems(d["extracts"], d["tex_sources"], d["formula_images"]))
    if problems:
        raise SystemExit("checks failed:\n  " + "\n  ".join(problems))


def caption(d, name):
    return next(c["text"] for c in d["claims"] if c["id"] == f"caption_{name}")


def tables(d, facts):
    """{table id: (header, rows)} with markdown cells."""
    g = analyze.grid(d["cells"])
    grid = contrasts.code_grid(d["codes"])
    TL = [s["id"] for s in d["settings"] if s["phase"] == "training" and s["culture"] == "LLM"]
    DL = [s["id"] for s in d["settings"] if s["phase"] == "deployment" and s["culture"] == "LLM"]
    T = [s["id"] for s in d["settings"] if s["phase"] == "training"]
    D = [s["id"] for s in d["settings"] if s["phase"] == "deployment"]
    lines = ["inside_the_box", "opening_sentence", "validation", "instruments", "where_the_hard_part_goes", "population"]
    cult = {(c["culture"], c["line"]): c["text"] for c in d["cultures"]}
    cultures = ["data-modeling", "algorithmic", "objective-modeling", "behavior-modeling"]
    cen = d["census"]["cross_citation"]
    return {
        "settings": (["Setting", "Phase", "Posed as", "Reward source", "One action is"],
                     [[s["id"], s["phase"], s["posed_as"], s["reward_source"], s["action_unit"]] for s in d["settings"]]),
        "primitives": (["Primitive", "In Sutton and Barto"], [[p["label"], p["rl_definition"]] for p in d["primitives"]]),
        "primitive_cells_training": (["Primitive"] + T, [[p["label"]] + [g[(p["id"], s)] for s in T] for p in d["primitives"]]),
        "primitive_cells_deployment": (["Primitive"] + D, [[p["label"]] + [g[(p["id"], s)] for s in D] for p in d["primitives"]]),
        "assumptions": (["\\#", "Assumption", "RL-agent default", "LLM-agent default", "Held by"],
                        [[a["id"], a["question"], a["rl_default"], a["llm_default"], a["owner"]] for a in d["assumptions"]]),
        "cultures": (["Line"] + cultures, [[ln.replace("_", " ")] + [cult.get((c, ln), "") for c in cultures] for ln in lines]),
        "census": (["", "Safe RL corpus", "LLM-agent-safety corpus"],
                   [["Works", facts["corpus_a_n"], facts["corpus_b_n"]],
                    ["References landing in own corpus", facts["a_refs_to_a"], facts["b_refs_to_b"]],
                    ["References landing in the other corpus", facts["a_refs_to_b"], facts["b_refs_to_a"]],
                    ["Papers citing the other corpus at all", facts["a_papers_citing_b"], facts["b_papers_citing_a"]]]),
        "gap": (["Property", "RL training", "LLM training", "RL deployment", "LLM deployment", "Moves with"],
                [[p["phrase"], grid[(p["id"], "T-RL")], contrasts.summarise(grid, p["id"], TL), grid[(p["id"], "D-RL")],
                  contrasts.summarise(grid, p["id"], DL), contrasts.attribution(grid, p["id"], d["pairs"], d["settings"])["label"]]
                 for p in d["properties"]]),
        "census_general": (["", "RL-agent corpus", "LLM-agent corpus"],
                           [["Works", facts.get("gen_corpus_a_n", ""), facts.get("gen_corpus_b_n", "")],
                            ["References landing in own corpus", facts.get("gen_a_refs_to_a", ""), facts.get("gen_b_refs_to_b", "")],
                            ["References landing in the other corpus", facts.get("gen_a_refs_to_b", ""), facts.get("gen_b_refs_to_a", "")],
                            ["Papers citing the other corpus at all", facts.get("gen_a_papers_citing_b", ""), facts.get("gen_b_papers_citing_a", "")]]),
        "coverage": (["Could a rule written before deployment have blocked the first-order harm?", "All, rater A", "All, rater B", "Deployer-operated, rater B"],
                     [["Yes", facts["writable_yes_h"], facts["writable_yes_s"], ""],
                      ["Partial", facts["writable_partial_h"], facts["writable_partial_s"], ""],
                      ["No", facts["writable_no_h"], facts["writable_no_s"], facts["writable_no_deployer"]]]),
        "incidents": (["Id", "Date", "Product", "Setting", "Trigger", "Approval gate", "Assumption tags"],
                      [[i["id"], i["date"], i["product"], i["setting"], i["trigger"], i["approval_gate"], i["assumption_tags"].replace(",", ", ")] for i in d["incidents"]]),
    }


def table_block(d, name, header, rows, longtable=False):
    flat = pandoc_many(header + [c for r in rows for c in r])
    h, body = flat[:len(header)], flat[len(header):]
    n = len(header)
    latex = render.table_latex(caption(d, name), f"tab:{name}", h, [body[i:i + n] for i in range(0, len(body), n)])
    if longtable:
        latex = latex.replace(r"\begin{table}[!htb]", r"\begin{table}[!htb]\footnotesize")
    return "\n```{=latex}\n" + latex + "\n```\n"


def appendix(d):
    by_prim = {}
    for c in d["cells"]:
        by_prim.setdefault(c["primitive"], []).append(c)
    label = {p["id"]: p["label"] for p in d["primitives"]}
    parts = []
    for p in d["primitives"]:
        bullets = "\n".join(f"- {c['setting']}, *{c['value']}*: {c['reason']}" for c in by_prim[p["id"]])
        parts.append(f"**{label[p['id']]}.**\n\n{bullets}")
    return "\n\n".join(parts)


def bibitems(refs, cited):
    labels = render.natbib_labels(refs)
    used = sorted((r for r in refs if r["key"] in cited), key=lambda r: (r["short"].lower(), r["year"], r["key"]))
    texts = pandoc_many([render.wrap_bare_urls(r["text"]) for r in used])
    return "\n".join(f"\\bibitem[{labels[r['key']]}]{{{r['key']}}} {t}" for r, t in zip(used, texts))


def main():
    d = load()
    run_checks(d)
    evidence, _, prose = quote_uses(d)
    (HERE / "out").mkdir(exist_ok=True)
    by_type = {t: sum(c["evidence_type"] == t for c in d["cells"]) for t in sorted(checks.EVIDENCE_TYPES)}
    summary = "Evidence for the primitive cells: " + "; ".join(f"{t} {n}" for t, n in by_type.items()) + ".\n\n"
    (HERE / "out" / "contrasts.md").write_text(contrast_report(d))
    (HERE / "out" / "backcheck.md").write_text(summary + backcheck.report(d["extracts"], evidence + prose, d["fulltexts"], d["manifest"]))
    facts = analyze.main()
    if d["census_general"] is None:
        raise SystemExit("080_census/general/metrics.json is missing: run 080_census/census.py general/config.json")
    (HERE / "out" / "sensitivity.md").write_text((ROOT / "100_analysis/sensitivity.md").read_text())
    tabs = tables(d, facts)
    set_phrases = {c["id"]: c["text"] for c in d["claims"] if c["kind"] in ("set", "scope", "contrast")}   # set phrases, the scope line and contrast claims are verified claims
    resolvers = {
        "fact": lambda k: facts[k] if k in facts else set_phrases[k],
        "table": lambda k: table_block(d, k, *tabs[k], longtable=(k == "incidents")),
        "include": lambda k: d[k],
        "appendix": lambda k: appendix(d),
    }
    title, abstract, body, app = render.split_draft(d["draft"])
    abstract_tex, body_tex, app_tex = (pandoc(render.expand(x, resolvers)) for x in (abstract, body, app))
    cited = render.latex_cite_keys(abstract_tex + body_tex + app_tex)
    tex = (HERE / "template.tex").read_text()
    for k, v in {"%%HEADSTART%%": r"\onecolumn", "%%HEADEND%%": "", "%%TITLE%%": title,
                 "%%RUNNING%%": RUNNING_TITLE, "%%ABSTRACT%%": abstract_tex, "%%BODY%%": body_tex,
                 "%%APPENDIX%%": app_tex, "%%BIBITEMS%%": bibitems(d["refs"], cited)}.items():
        tex = tex.replace(k, v)
    out = HERE / "out"
    (out / "paper.tex").write_text(tex)
    env = {**os.environ, "TEXINPUTS": f"{HERE}:"}
    for _ in range(2):
        run = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=out,
                             capture_output=True, text=True, errors="replace", env=env)
        if run.returncode != 0:
            print(run.stdout[-3000:])
            raise SystemExit("pdflatex failed")
    log = (out / "paper.log").read_text(errors="replace")
    if "undefined" in log or "Overfull" in log:
        raise SystemExit("LaTeX reports undefined references or overfull boxes; see out/paper.log")
    print("wrote", out / "paper.pdf", "|", len(cited), "of", len(d["refs"]), "references cited")


if __name__ == "__main__":
    main()
