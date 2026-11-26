"""Check that each reference exists: look up its arXiv id or DOI and compare the title and first author.

Writes existence.csv (the cache that the build reads; the build makes no network calls).
Usage: python3 verify.py [key ...]     (no key: every reference not yet checked)
A reference without arXiv id or DOI is checked against the full text we hold (045_fulltext), else against its URL.
Status: ok | mismatch | not_found | unverified (the URL did not answer or does not show the title: check by hand
and set status to manual with a note).
"""
from pathlib import Path
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import yaml

HERE = Path(__file__).resolve().parent
FIELDS = ["key", "id", "registry", "found_title", "found_first_author", "found_year", "title_overlap", "status", "checked_on", "note"]
AGENT = {"User-Agent": "reference-existence-check/1.0"}
ARXIV = re.compile(r"arxiv\.org/abs/([\w.\-/]+?)(?:v\d+)?(?=$|[\s)\]])")
DOI = re.compile(r"doi\.org/(10\.\S+)")          # a DOI may contain parentheses; it ends at whitespace
URL = re.compile(r"https?://\S+")
MIN_OVERLAP = 0.6


def identifier(text):
    """('arxiv'|'doi', id) from a reference text, or (None, None)."""
    for registry, pattern in (("arxiv", ARXIV), ("doi", DOI)):
        m = pattern.search(text)
        if m:
            return registry, m.group(1).rstrip(".,;")
    m = URL.search(text)
    return ("url", m.group(0).rstrip(".,;")) if m else (None, None)


def cited_title(text):
    """Title as cited: the first quoted string, else the first italic string."""
    m = re.search(r'"([^"]+)"', text) or re.search(r"\*([^*]+)\*", text)
    return m.group(1).rstrip(",.") if m else ""


def words(title):
    return set(re.findall(r"[a-z0-9]+", title.lower())) - {"a", "an", "the", "of", "for", "in", "on", "and", "to", "with"}


def overlap(cited, found):
    """Share of the cited title's words that the found title has (0..1)."""
    c, f = words(cited), words(found)
    return round(len(c & f) / len(c), 2) if c else 0.0


def judge(ref_text, found_title, found_author):
    """Status from the cited text and the registry record."""
    if not found_title:
        return "not_found"
    surname = found_author.split()[-1].lower() if found_author else ""
    author_ok = bool(surname) and surname in ref_text.lower()
    return "ok" if overlap(cited_title(ref_text), found_title) >= MIN_OVERLAP and author_ok else "mismatch"


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=60) as r:
        return r.read()


def lookup_arxiv(ids):
    """{id: (title, first author, year)} for up to 50 arXiv ids in one call."""
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(fetch("http://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids)))
    out = {}
    for e in root.findall("a:entry", ns):
        found = re.sub(r"v\d+$", "", e.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1])
        out[found] = (re.sub(r"\s+", " ", e.findtext("a:title", "", ns)).strip(),
                      e.findtext("a:author/a:name", "", ns), e.findtext("a:published", "", ns)[:4])
    return out


def lookup_doi(doi):
    try:
        m = json.loads(fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    except Exception:
        return ("", "", "")
    author = (m.get("author") or m.get("editor") or [{}])[0]
    year = str((m.get("issued", {}).get("date-parts") or [[""]])[0][0])
    return ((m.get("title") or [""])[0], f"{author.get('given', '')} {author.get('family', '')}".strip(), year)


def lookup_held(key):
    """Opening of the full text we hold for this key, or "" if we hold none."""
    path = HERE.parent / "045_fulltext" / f"{key}.txt"
    return path.read_text(errors="replace")[:5000] if path.exists() else ""


def lookup_url(url):
    """Visible text of the page at `url`, or "" if it does not answer."""
    try:
        return re.sub(r"<[^>]+>", " ", fetch(url).decode("utf-8", "replace"))
    except Exception:
        return ""


def judge_page(ref_text, page):
    """ok if the page shows the cited title; unverified otherwise."""
    return "ok" if page and overlap(cited_title(ref_text), page) >= 0.9 else "unverified"


def main(keys, today):
    refs = yaml.safe_load((HERE / "refs.yaml").read_text())
    path = HERE / "existence.csv"
    done = {r["key"]: r for r in csv.DictReader(open(path, newline=""))} if path.exists() else {}
    todo = [r for r in refs if (r["key"] in keys if keys else r["key"] not in done)]
    ids = {r["key"]: identifier(r["text"]) for r in todo}
    arxiv_ids = [i for reg, i in ids.values() if reg == "arxiv"]
    found = {}
    for n in range(0, len(arxiv_ids), 50):
        found.update(lookup_arxiv(arxiv_ids[n:n + 50]))
        time.sleep(4)
    for r in todo:
        registry, ident = ids[r["key"]]
        title, author, year = found.get(ident, ("", "", "")) if registry == "arxiv" else lookup_doi(ident) if registry == "doi" else ("", "", "")
        if registry in ("arxiv", "doi"):
            status = judge(r["text"], title, author)
        else:
            held = lookup_held(r["key"])
            registry, status = ("held", judge_page(r["text"], held)) if held else ("url", judge_page(r["text"], lookup_url(ident) if ident else ""))
            title = cited_title(r["text"]) if status == "ok" else ""
        done[r["key"]] = {"key": r["key"], "id": ident or "", "registry": registry or "", "found_title": title,
                          "found_first_author": author, "found_year": year, "title_overlap": overlap(cited_title(r["text"]), title),
                          "status": status, "checked_on": today, "note": ""}
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(done[r["key"]] for r in refs if r["key"] in done)
    counts = {}
    for row in done.values():
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(counts)


if __name__ == "__main__":
    main(sys.argv[1:], time.strftime("%Y-%m-%d"))
