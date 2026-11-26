#!/usr/bin/env python3
"""Citation census of two literatures via the OpenAlex API.

Corpus A: safe RL / objective-modeling.   Corpus B: LLM-agent safety / behavior-modeling.
Measures cross-citation, author overlap, venue overlap, community structure, time series,
and citation of canonical works. Every API response is cached on disk, so re-runs are free.

Layout (Lakos levelization, low to high):
  1. config          constants, queries, paths
  2. openalex client disk-cached HTTP with retry (the only I/O adapter)
  3. corpus          fetch + slim + dedup + eligibility (imperative shell)
  4. measures        pure functions over slim work records (functional core)
  5. outputs         CSV / JSON / markdown tables
  6. main
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import requests

# ----------------------------------------------------------------------------- 1. config

MAILTO = os.environ.get("OPENALEX_MAILTO", "")   # OpenAlex polite-pool contact; set it in the environment
BASE = "https://api.openalex.org"
YEARS = "2012-2026"
# OpenAlex primary_topic.field: 17 = Computer Science, 22 = Engineering. Drops stemmed matches from
# agriculture, geology, forensics etc. ("AI control" of a litter agitator, "safe exploration" of hydrogen).
FIELDS = "fields/17|fields/22"
PER_PAGE = 200            # one page per query keeps the call count small
PAGES_PER_QUERY = 1
SLEEP_S = 0.25            # stay well under 10 req/s
SELECT = "id,doi,title,publication_year,cited_by_count,primary_location,authorships,referenced_works,topics"

OUT_DIR = Path(__file__).resolve().parent
CACHE_DIR = Path(
    "/tmp/claude-1000/-usr-local-HAMMER-DYNAMIC-SRC-pathway-PERSONAL-PUZZLES-PERSONAL-RESEARCH-AGENDAS"
    "-ML-RL-safety-paper--two-cultures/0f0b889d-e931-4f68-9b4f-82720df26b60/scratchpad/census/cache"
)

QUERIES_A = [
    "safe reinforcement learning",
    "constrained Markov decision process",
    "constrained policy optimization",
    "shielding reinforcement learning",
    "safe exploration",
    "reward misspecification reinforcement learning",
    "reward hacking",
]
QUERIES_B = [
    "LLM agent safety",
    "prompt injection",
    "indirect prompt injection",
    "jailbreak LLM agents",
    "agent red teaming",
    "alignment faking",
    "scheming language models",
    "AI control",
    "sycophancy language models",
    "agentic misalignment",
    "tool-use agent safety",
]
# Robustness: narrower, more technical phrasings.
NARROW_A = ["constrained policy optimization", "shielding reinforcement learning", "safe exploration Markov decision process"]
NARROW_B = ["indirect prompt injection", "alignment faking", "jailbreak LLM agents"]

# Canonical works: OpenAlex id or DOI (single-entity lookups are free). Safety Gym has no DOI -> title search.
CANON_A = {
    "Achiam et al. 2017 Constrained Policy Optimization": "https://doi.org/10.48550/arXiv.1705.10528",
    "Alshiekh et al. 2018 Safe RL via Shielding": "https://doi.org/10.48550/arXiv.1708.08611",
    "Moldovan & Abbeel 2012 Safe Exploration in MDPs": "https://doi.org/10.48550/arXiv.1205.4810",
    # Safety Gym (OpenAI report, no DOI/arXiv) - title searches for the full title and "Safety Gym" both return 0 hits.
    "Ray, Achiam, Amodei 2019 Safety Gym": "title:Benchmarking Safe Exploration in Deep Reinforcement Learning",
    "Garcia & Fernandez 2015 survey": "W1845972764",
    "Amodei et al. 2016 Concrete Problems": "https://doi.org/10.48550/arXiv.1606.06565",
}
CANON_B = {
    "Greshake et al. 2023 indirect prompt injection": "https://doi.org/10.48550/arXiv.2302.12173",
    "Debenedetti et al. 2024 AgentDojo": "https://doi.org/10.48550/arXiv.2406.13352",
    "Greenblatt et al. 2024 Alignment Faking": "https://doi.org/10.48550/arXiv.2412.14093",
    "Greenblatt et al. 2023 AI Control": "https://doi.org/10.48550/arXiv.2312.06942",
    "Meinke et al. 2024 In-context scheming": "https://doi.org/10.48550/arXiv.2412.04984",
}
# Known duplicate OpenAlex records (conference versions) of canonical works, appended after lookup.
CANON_EXTRA_DOIS = {
    "Alshiekh et al. 2018 Safe RL via Shielding": ["https://doi.org/10.1609/aaai.v32i1.11797"],
    "Greshake et al. 2023 indirect prompt injection": ["https://doi.org/10.1145/3605764.3623985"],
}

# ----------------------------------------------------------------------------- 2. openalex client

FAILURES: list[dict] = []


def _cache_path(url: str, params: dict) -> Path:
    key = hashlib.sha1((url + json.dumps(params, sort_keys=True)).encode()).hexdigest()
    return CACHE_DIR / f"{key}.json"


def oa_get(path: str, params: dict | None = None, retries: int = 5) -> dict | None:
    """GET with disk cache and exponential backoff. Returns parsed JSON or None (failure recorded)."""
    params = dict(params or {})
    if MAILTO:
        params["mailto"] = MAILTO
    url = path if path.startswith("http") else BASE + path
    cp = _cache_path(url, params)
    if cp.exists():
        return json.loads(cp.read_text())
    delay = 1.0
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=60)
        except requests.RequestException as e:
            FAILURES.append({"url": url, "params": params, "attempt": attempt, "error": str(e)})
            time.sleep(delay); delay *= 2; continue
        if r.status_code == 200:
            data = r.json()
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cp.write_text(json.dumps(data))
            cost = data.get("meta", {}).get("cost_usd")
            print(f"  GET {path} {json.dumps({k: v for k, v in params.items() if k != 'mailto'})[:90]} -> 200 cost={cost}", file=sys.stderr)
            time.sleep(SLEEP_S)
            return data
        if r.status_code == 404:
            FAILURES.append({"url": url, "params": params, "status": 404})
            return None
        FAILURES.append({"url": url, "params": params, "attempt": attempt, "status": r.status_code, "body": r.text[:300]})
        if r.status_code in (429, 500, 502, 503):
            wait = float(r.headers.get("Retry-After", delay))
            time.sleep(min(wait, 60)); delay *= 2; continue
        return None
    return None


def oa_search(query: str, pages: int = PAGES_PER_QUERY) -> list[dict]:
    """Title+abstract search, relevance order, cursor paging."""
    results, cursor = [], "*"
    for _ in range(pages):
        data = oa_get("/works", {
            "filter": f'title_and_abstract.search:"{query}",publication_year:{YEARS},type:article|preprint,language:en,primary_topic.field.id:{FIELDS}',
            "per-page": PER_PAGE, "cursor": cursor, "select": SELECT,
        })
        if not data:
            break
        results.extend(data["results"])
        cursor = data["meta"].get("next_cursor")
        if not cursor:
            break
    return results


def oa_work(ref: str) -> dict | None:
    """Resolve an OpenAlex id, DOI, or 'title:...' to a work (id lookups are free)."""
    sel = "id,doi,title,publication_year,cited_by_count"
    if ref.startswith("title:"):
        data = oa_get("/works", {"filter": f'title.search:"{ref[6:]}"', "per-page": 5, "select": sel})
        return (data or {}).get("results", [None])[0] if data and data["results"] else None
    return oa_get(f"/works/{ref}", {"select": sel})

# ----------------------------------------------------------------------------- 3. corpus


def slim(w: dict, query: str) -> dict:
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return {
        "id": w["id"],
        "doi": w.get("doi"),
        "title": w.get("title") or "",
        "year": w.get("publication_year"),
        "venue": src.get("display_name") or "",
        "venue_id": src.get("id") or "",
        "cited_by_count": w.get("cited_by_count", 0),
        "authors": [(a["author"]["id"], a["author"].get("display_name", "")) for a in w.get("authorships", []) if a.get("author", {}).get("id")],
        "refs": w.get("referenced_works", []) or [],
        "topics": [t["display_name"] for t in (w.get("topics") or [])[:3]],
        "queries": [query],
    }


def eligible(w: dict) -> bool:
    return (w["cited_by_count"] or 0) >= 1 or (w["year"] or 0) >= 2024


def fetch_corpus(queries: list[str]) -> dict[str, dict]:
    corpus: dict[str, dict] = {}
    for q in queries:
        for raw in oa_search(q):
            s = slim(raw, q)
            if not eligible(s):
                continue
            if s["id"] in corpus:
                corpus[s["id"]]["queries"].append(q)
            else:
                corpus[s["id"]] = s
    return corpus


def split_bridge(A: dict, B: dict) -> tuple[dict, dict, dict]:
    bridge_ids = set(A) & set(B)
    bridge = {i: {**A[i], "queries": sorted(set(A[i]["queries"] + B[i]["queries"]))} for i in bridge_ids}
    return ({i: w for i, w in A.items() if i not in bridge_ids},
            {i: w for i, w in B.items() if i not in bridge_ids}, bridge)

# ----------------------------------------------------------------------------- 4. measures (pure)


def ref_landing(src: dict, A: dict, B: dict) -> dict:
    """Where do the references of `src` land? Counts with denominators."""
    total = sum(len(w["refs"]) for w in src.values())
    in_a = sum(1 for w in src.values() for r in w["refs"] if r in A)
    in_b = sum(1 for w in src.values() for r in w["refs"] if r in B)
    return {"total_refs": total, "to_A": in_a, "to_B": in_b,
            "frac_to_A": in_a / total if total else None, "frac_to_B": in_b / total if total else None,
            "papers": len(src), "papers_citing_A": sum(1 for w in src.values() if any(r in A for r in w["refs"])),
            "papers_citing_B": sum(1 for w in src.values() if any(r in B for r in w["refs"]))}


def cross_citation(A: dict, B: dict) -> dict:
    a, b = ref_landing(A, A, B), ref_landing(B, A, B)
    in_corpus_a, in_corpus_b = a["to_A"] + a["to_B"], b["to_A"] + b["to_B"]
    return {
        "A": {**a, "within": a["to_A"], "cross": a["to_B"], "in_corpus_refs": in_corpus_a,
              "cross_share_of_in_corpus": a["to_B"] / in_corpus_a if in_corpus_a else None},
        "B": {**b, "within": b["to_B"], "cross": b["to_A"], "in_corpus_refs": in_corpus_b,
              "cross_share_of_in_corpus": b["to_A"] / in_corpus_b if in_corpus_b else None},
    }


def author_overlap(A: dict, B: dict) -> dict:
    def authors(C):
        cnt, names = Counter(), {}
        for w in C.values():
            for aid, name in set(w["authors"]):
                cnt[aid] += 1; names[aid] = name
        return cnt, names
    ca, na = authors(A); cb, nb = authors(B)
    both = set(ca) & set(cb)
    top = sorted(both, key=lambda i: -(ca[i] + cb[i]))[:20]
    return {"authors_A": len(ca), "authors_B": len(cb), "authors_both": len(both),
            "frac_of_A_authors": len(both) / len(ca) if ca else None,
            "frac_of_B_authors": len(both) / len(cb) if cb else None,
            "jaccard": len(both) / len(set(ca) | set(cb)) if ca or cb else None,
            "papers_A_with_bridging_author": sum(1 for w in A.values() if any(a in both for a, _ in w["authors"])),
            "papers_B_with_bridging_author": sum(1 for w in B.values() if any(a in both for a, _ in w["authors"])),
            "top_bridging": [{"id": i, "name": na.get(i) or nb.get(i), "papers_A": ca[i], "papers_B": cb[i]} for i in top]}


def venue_overlap(A: dict, B: dict, top_n: int = 15) -> dict:
    va = Counter(w["venue"] for w in A.values() if w["venue"]); vb = Counter(w["venue"] for w in B.values() if w["venue"])
    def jacc(x, y): return len(x & y) / len(x | y) if (x | y) else None
    va2 = {v for v, c in va.items() if c >= 2}; vb2 = {v for v, c in vb.items() if c >= 2}
    return {"top_A": va.most_common(top_n), "top_B": vb.most_common(top_n),
            "n_venues_A": len(va), "n_venues_B": len(vb), "shared": len(set(va) & set(vb)),
            "jaccard_all": jacc(set(va), set(vb)), "jaccard_min2": jacc(va2, vb2), "shared_min2": sorted(va2 & vb2),
            "no_venue_A": sum(1 for w in A.values() if not w["venue"]), "no_venue_B": sum(1 for w in B.values() if not w["venue"])}


def union_graph(A: dict, B: dict) -> nx.Graph:
    G = nx.Graph()
    for lab, C in (("A", A), ("B", B)):
        for i in C:
            G.add_node(i, label=lab)
    for C in (A, B):
        for i, w in C.items():
            for r in w["refs"]:
                if r in G and r != i:
                    G.add_edge(i, r)
    return G


def nmi(labels_true: list, labels_pred: list) -> float:
    n = len(labels_true)
    ct = Counter(zip(labels_true, labels_pred)); ca = Counter(labels_true); cb = Counter(labels_pred)
    mi = sum(c / n * math.log((c * n) / (ca[a] * cb[b])) for (a, b), c in ct.items())
    ha = -sum(c / n * math.log(c / n) for c in ca.values()); hb = -sum(c / n * math.log(c / n) for c in cb.values())
    return 2 * mi / (ha + hb) if (ha + hb) else 0.0


def community_structure(A: dict, B: dict, seed: int = 0) -> dict:
    G = union_graph(A, B)
    isolated = [n for n in G if G.degree(n) == 0]
    H = G.subgraph([n for n in G if G.degree(n) > 0]).copy()
    comms = nx.community.louvain_communities(H, seed=seed)
    comm_of = {n: k for k, c in enumerate(comms) for n in c}
    nodes = list(H)
    true = [H.nodes[n]["label"] for n in nodes]; pred = [comm_of[n] for n in nodes]
    purity = sum(max(Counter(H.nodes[n]["label"] for n in c).values()) for c in comms) / len(nodes)
    ab_partition = [{n for n in H if H.nodes[n]["label"] == "A"}, {n for n in H if H.nodes[n]["label"] == "B"}]
    ab_partition = [p for p in ab_partition if p]
    works = {**A, **B}
    comm_rows = []
    for k, c in sorted(enumerate(comms), key=lambda kc: -len(kc[1]))[:10]:
        lab = Counter(H.nodes[n]["label"] for n in c)
        qs = Counter(q for n in c for q in works[n]["queries"]).most_common(3)
        comm_rows.append({"community": k, "size": len(c), "A": lab["A"], "B": lab["B"],
                          "top_queries": "; ".join(f"{q} ({m})" for q, m in qs)})
    cross_edges = sum(1 for u, v in H.edges if H.nodes[u]["label"] != H.nodes[v]["label"])
    comps = list(nx.connected_components(H))
    return {"nodes_total": G.number_of_nodes(), "isolated_nodes": len(isolated), "nodes_connected": H.number_of_nodes(),
            "edges": H.number_of_edges(), "cross_label_edges": cross_edges,
            "cross_edge_frac": cross_edges / H.number_of_edges() if H.number_of_edges() else None,
            "n_communities": len(comms), "purity": purity, "nmi": nmi(true, pred),
            "modularity_louvain": nx.community.modularity(H, comms),
            "modularity_AB_labels": nx.community.modularity(H, ab_partition) if len(ab_partition) == 2 else None,
            "n_components": len(comps), "largest_component": max((len(c) for c in comps), default=0),
            "largest_communities": comm_rows}


def time_series(A: dict, B: dict) -> list[dict]:
    rows = []
    for y in sorted({w["year"] for w in list(A.values()) + list(B.values()) if w["year"]}):
        By = {i: w for i, w in B.items() if w["year"] == y}; Ay = {i: w for i, w in A.items() if w["year"] == y}
        b, a = ref_landing(By, A, B), ref_landing(Ay, A, B)
        rows.append({"year": y, "B_papers": len(By), "B_refs": b["total_refs"], "B_to_A": b["to_A"], "B_to_B": b["to_B"],
                     "B_to_A_rate": b["frac_to_A"], "B_papers_citing_A": b["papers_citing_A"],
                     "A_papers": len(Ay), "A_refs": a["total_refs"], "A_to_B": a["to_B"], "A_to_A": a["to_A"],
                     "A_to_B_rate": a["frac_to_B"], "A_papers_citing_B": a["papers_citing_B"]})
    return rows


def canonical_check(canon_ids: dict[str, list[str]], citing_corpus: dict) -> dict:
    rows, any_set = [], set()
    for name, ids in canon_ids.items():
        citers = {i for i, w in citing_corpus.items() if any(r in ids for r in w["refs"])}
        any_set |= citers
        rows.append({"work": name, "openalex_ids": ids, "citers": len(citers)})
    return {"rows": rows, "papers_citing_any": len(any_set), "denominator": len(citing_corpus),
            "frac": len(any_set) / len(citing_corpus) if citing_corpus else None}


def cross_by_query(src: dict, dst: dict) -> list[tuple[str, int]]:
    """Attribute cross-corpus citations to the queries that matched the citing paper."""
    c = Counter(q for w in src.values() for r in w["refs"] if r in dst for q in w["queries"])
    return c.most_common()


def without_query(C: dict, query: str) -> dict:
    """Drop works whose only matching query is `query`."""
    return {i: w for i, w in C.items() if w["queries"] != [query]}


def cited_only(C: dict) -> dict:
    return {i: w for i, w in C.items() if (w["cited_by_count"] or 0) >= 1}


def sensitivity(A: dict, B: dict) -> dict:
    A_no_rh = without_query(A, "reward hacking")
    Ac, Bc = cited_only(A), cited_only(B)
    return {
        "cross_by_query": {"A_to_B": cross_by_query(A, B), "B_to_A": cross_by_query(B, A)},
        "A_without_reward_hacking": {"sizes": {"A": len(A_no_rh), "B": len(B)}, "cross_citation": cross_citation(A_no_rh, B),
                                     "community": community_structure(A_no_rh, B)},
        "cited_only": {"sizes": {"A": len(Ac), "B": len(Bc)}, "cross_citation": cross_citation(Ac, Bc),
                       "community": community_structure(Ac, Bc)},
    }


def resolve_canon(canon: dict[str, str]) -> tuple[dict[str, list[str]], dict[str, dict]]:
    ids, meta = {}, {}
    for name, ref in canon.items():
        w = oa_work(ref)
        found = [w["id"]] if w else []
        meta[name] = w or {"error": "not found", "ref": ref}
        for extra in CANON_EXTRA_DOIS.get(name, []):
            we = oa_work(extra)
            if we and we["id"] not in found:
                found.append(we["id"])
        ids[name] = found
    return ids, meta

# ----------------------------------------------------------------------------- 5. outputs


def write_corpus_csv(path: Path, C: dict, label: str) -> None:
    with path.open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["corpus", "id", "doi", "title", "year", "venue", "cited_by_count", "n_refs", "authors", "topics", "matched_queries"])
        for w in sorted(C.values(), key=lambda w: -(w["cited_by_count"] or 0)):
            wr.writerow([label, w["id"], w["doi"] or "", w["title"], w["year"], w["venue"], w["cited_by_count"], len(w["refs"]),
                         "; ".join(f"{i}|{n}" for i, n in w["authors"]), "; ".join(w["topics"]), "; ".join(w["queries"])])


def pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def bar(frac: float, width: int = 40) -> str:
    n = int(round((frac or 0) * width))
    return "#" * n + "." * (width - n)


def tables_md(m: dict) -> str:
    cc, au, ve, co, ts, cz = m["cross_citation"], m["author_overlap"], m["venue_overlap"], m["community"], m["time_series"], m["canonical"]
    L = ["# Census tables (generated by census.py)\n", f"Generated {m['generated']}. API failures recorded: {m['n_failures']}.\n"]
    L += ["## Corpus sizes\n", "| set | works | total refs |", "|---|---|---|"]
    for k in ("A", "B"):
        L.append(f"| {k} | {m['sizes'][k]} | {cc[k]['total_refs']} |")
    L.append(f"| bridge (matched both) | {m['sizes']['bridge']} | |\n")
    L += ["## 2a Cross-citation\n", "| from | total refs | within corpus | cross corpus | cross/total | cross/in-corpus | papers citing other corpus |", "|---|---|---|---|---|---|---|"]
    for k, other in (("A", "B"), ("B", "A")):
        c = cc[k]
        L.append(f"| {k} -> {other} | {c['total_refs']} | {c['within']} ({pct(c['within']/c['total_refs'] if c['total_refs'] else None)}) | {c['cross']} ({pct(c['cross']/c['total_refs'] if c['total_refs'] else None)}) | {pct(c['frac_to_B'] if k=='A' else c['frac_to_A'])} | {pct(c['cross_share_of_in_corpus'])} | {c['papers_citing_B'] if k=='A' else c['papers_citing_A']} / {c['papers']} |")
    L.append("\n```")
    for k in ("A", "B"):
        c = cc[k]; t = c["total_refs"] or 1
        L.append(f"{k} refs -> within {k}   {bar(c['within']/t)} {pct(c['within']/t)}")
        L.append(f"{k} refs -> other       {bar(c['cross']/t)} {pct(c['cross']/t)}")
        L.append(f"{k} refs -> outside     {bar((t-c['within']-c['cross'])/t)} {pct((t-c['within']-c['cross'])/t)}")
    L.append("```\n")
    L += ["## 2b Author overlap\n", f"- authors in A: {au['authors_A']}; in B: {au['authors_B']}; in both: {au['authors_both']} "
          f"({pct(au['frac_of_A_authors'])} of A authors, {pct(au['frac_of_B_authors'])} of B authors; Jaccard {au['jaccard']:.4f})",
          f"- papers with at least one bridging author: A {au['papers_A_with_bridging_author']}/{m['sizes']['A']}, B {au['papers_B_with_bridging_author']}/{m['sizes']['B']}\n",
          "| bridging author | OpenAlex id | papers in A | papers in B |", "|---|---|---|---|"]
    L += [f"| {r['name']} | {r['id']} | {r['papers_A']} | {r['papers_B']} |" for r in au["top_bridging"]]
    L += ["\n## 2c Venue overlap\n", f"- distinct venues: A {ve['n_venues_A']}, B {ve['n_venues_B']}, shared {ve['shared']}; Jaccard(all) {ve['jaccard_all']:.4f}; Jaccard(venues with >=2 papers) {ve['jaccard_min2']:.4f}",
          f"- works with no venue: A {ve['no_venue_A']}, B {ve['no_venue_B']}", f"- shared venues with >=2 papers in each: {', '.join(ve['shared_min2']) or 'none'}\n",
          "| rank | top venue A | n | top venue B | n |", "|---|---|---|---|---|"]
    for i in range(15):
        a = ve["top_A"][i] if i < len(ve["top_A"]) else ("", ""); b = ve["top_B"][i] if i < len(ve["top_B"]) else ("", "")
        L.append(f"| {i+1} | {a[0]} | {a[1]} | {b[0]} | {b[1]} |")
    L += ["\n## 2d Community structure (Louvain, networkx, seed 0)\n",
          f"- nodes {co['nodes_total']} (isolated, no in-corpus edge: {co['isolated_nodes']}); connected nodes {co['nodes_connected']}; edges {co['edges']}; cross-label edges {co['cross_label_edges']} ({pct(co['cross_edge_frac'])})",
          f"- components {co['n_components']}, largest {co['largest_component']}",
          f"- Louvain communities {co['n_communities']}; purity vs A/B labels {co['purity']:.3f}; NMI {co['nmi']:.3f}",
          f"- modularity: Louvain {co['modularity_louvain']:.3f}; A/B label partition {co['modularity_AB_labels'] if co['modularity_AB_labels'] is None else round(co['modularity_AB_labels'],3)}\n",
          "| community | size | A | B | top matched queries |", "|---|---|---|---|---|"]
    L += [f"| {r['community']} | {r['size']} | {r['A']} | {r['B']} | {r['top_queries']} |" for r in co["largest_communities"]]
    L += ["\n## 2e Time series\n", "| year | B papers | B refs | B->A | B->B | B->A rate | B papers citing A | A papers | A refs | A->B | A->A | A->B rate |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {r['year']} | {r['B_papers']} | {r['B_refs']} | {r['B_to_A']} | {r['B_to_B']} | {pct(r['B_to_A_rate'])} | {r['B_papers_citing_A']} | {r['A_papers']} | {r['A_refs']} | {r['A_to_B']} | {r['A_to_A']} | {pct(r['A_to_B_rate'])} |" for r in ts]
    L += ["\n## 2f Canonical works\n"]
    for k, other in (("B_cites_canonA", "B"), ("A_cites_canonB", "A")):
        c = cz[k]
        L += [f"### corpus {other} citing canonical works of the other culture: {c['papers_citing_any']} / {c['denominator']} ({pct(c['frac'])})\n", "| canonical work | OpenAlex ids | citers |", "|---|---|---|"]
        L += [f"| {r['work']} | {', '.join(r['openalex_ids']) or 'NOT FOUND'} | {r['citers']} |" for r in c["rows"]]
        L.append("")
    L += ["## 3 Robustness (narrow queries)\n", f"narrow A: {m['robustness']['queries_A']}; narrow B: {m['robustness']['queries_B']}; sizes A {m['robustness']['sizes']['A']}, B {m['robustness']['sizes']['B']}, bridge {m['robustness']['sizes']['bridge']}\n",
          "| from | total refs | within | cross | cross/total | cross/in-corpus |", "|---|---|---|---|---|---|"]
    for k, other in (("A", "B"), ("B", "A")):
        c = m["robustness"]["cross_citation"][k]; t = c["total_refs"] or 1
        L.append(f"| {k} -> {other} | {c['total_refs']} | {c['within']} | {c['cross']} | {pct(c['cross']/t)} | {pct(c['cross_share_of_in_corpus'])} |")
    se = m["sensitivity"]
    L += ["\n## 3b Sensitivity (same data, no new API calls)\n",
          "Cross-citations attributed to the citing paper's matched queries (a paper matching k queries counts k times):",
          f"- A -> B: {se['cross_by_query']['A_to_B']}", f"- B -> A: {se['cross_by_query']['B_to_A']}\n",
          "| variant | A | B | A->B cross/total | A->B cross/in-corpus | B->A cross/total | B->A cross/in-corpus | Louvain purity | NMI | cross-label edges |", "|---|---|---|---|---|---|---|---|---|---|"]
    for name, v in (("A without 'reward hacking'-only works", se["A_without_reward_hacking"]), ("cited >= 1 only", se["cited_only"])):
        ca, cb, co2 = v["cross_citation"]["A"], v["cross_citation"]["B"], v["community"]
        L.append(f"| {name} | {v['sizes']['A']} | {v['sizes']['B']} | {ca['cross']}/{ca['total_refs']} ({pct(ca['frac_to_B'])}) | {pct(ca['cross_share_of_in_corpus'])} | {cb['cross']}/{cb['total_refs']} ({pct(cb['frac_to_A'])}) | {pct(cb['cross_share_of_in_corpus'])} | {co2['purity']:.3f} | {co2['nmi']:.3f} | {co2['cross_label_edges']}/{co2['edges']} |")
    L += ["\n## Bridge set (matched queries of both corpora)\n", "| year | title | queries | OpenAlex |", "|---|---|---|---|"]
    L += [f"| {w['year']} | {w['title']} | {'; '.join(w['queries'])} | {w['id']} |" for w in sorted(m["bridge_list"], key=lambda w: (w["year"] or 0, w["title"]))]
    return "\n".join(L) + "\n"

# ----------------------------------------------------------------------------- 6. main


def run_pair(qa: list[str], qb: list[str]) -> tuple[dict, dict, dict]:
    return split_bridge(fetch_corpus(qa), fetch_corpus(qb))


def load_config(path: str) -> None:
    """Optional JSON {queries_A, queries_B, out_dir}: a second census with other queries writes to another folder."""
    global QUERIES_A, QUERIES_B, OUT_DIR
    cfg = json.loads(Path(path).read_text())
    QUERIES_A, QUERIES_B = cfg["queries_A"], cfg["queries_B"]
    OUT_DIR = (Path(path).resolve().parent / cfg.get("out_dir", ".")).resolve()
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if len(sys.argv) > 1:
        load_config(sys.argv[1])
    print("fetching primary corpora", file=sys.stderr)
    A, B, bridge = run_pair(QUERIES_A, QUERIES_B)
    print(f"A={len(A)} B={len(B)} bridge={len(bridge)}", file=sys.stderr)
    canon_a_ids, canon_a_meta = resolve_canon(CANON_A)
    canon_b_ids, canon_b_meta = resolve_canon(CANON_B)
    print("fetching narrow corpora", file=sys.stderr)
    nA, nB, nbridge = run_pair(NARROW_A, NARROW_B)

    metrics = {
        "generated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "queries": {"A": QUERIES_A, "B": QUERIES_B}, "years": YEARS, "per_query_cap": PER_PAGE * PAGES_PER_QUERY,
        "sizes": {"A": len(A), "B": len(B), "bridge": len(bridge)},
        "cross_citation": cross_citation(A, B),
        "author_overlap": author_overlap(A, B),
        "venue_overlap": venue_overlap(A, B),
        "community": community_structure(A, B),
        "time_series": time_series(A, B),
        "canonical": {"B_cites_canonA": canonical_check(canon_a_ids, B), "A_cites_canonB": canonical_check(canon_b_ids, A),
                      "canon_meta": {**canon_a_meta, **canon_b_meta}},
        "robustness": {"queries_A": NARROW_A, "queries_B": NARROW_B, "sizes": {"A": len(nA), "B": len(nB), "bridge": len(nbridge)},
                       "cross_citation": cross_citation(nA, nB), "community": community_structure(nA, nB)},
        "sensitivity": sensitivity(A, B),
        "bridge_list": [{"id": w["id"], "title": w["title"], "year": w["year"], "queries": w["queries"]} for w in bridge.values()],
        "n_failures": len(FAILURES),
    }
    write_corpus_csv(OUT_DIR / "corpus_A.csv", A, "A")
    write_corpus_csv(OUT_DIR / "corpus_B.csv", B, "B")
    write_corpus_csv(OUT_DIR / "bridge.csv", bridge, "bridge")
    (OUT_DIR / "metrics.json").write_text(json.dumps(metrics, indent=1, default=list))
    (OUT_DIR / "failures.json").write_text(json.dumps(FAILURES, indent=1))
    (OUT_DIR / "census_tables.md").write_text(tables_md(metrics))
    cc = metrics["cross_citation"]
    print(f"\nA={len(A)} B={len(B)} bridge={len(bridge)}  A->B {cc['A']['cross']}/{cc['A']['total_refs']}  B->A {cc['B']['cross']}/{cc['B']['total_refs']}  failures={len(FAILURES)}")


if __name__ == "__main__":
    main()
