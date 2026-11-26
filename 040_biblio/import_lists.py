"""One-off importer: numbered reference lists in the archived markdown files -> refs.yaml entries.

Two list formats are read:
  A  "N. Surname, I. & Surname, I. (Year). Title. *Venue*. URL"       (concept_semantics_expanded.md)
  B  "[N] I. Surname, I. Surname, "Title," *Venue*, Year. URL"         (twopager.md, assumptions_table.md, framing.md)
Keys are surname+year (+a/b when two works share them). A work already keyed in paper__debunking/040_biblio/refs.yaml
(same arXiv id or DOI) keeps that key. Entries the parser cannot read are listed in unparsed.txt for a hand pass.
Usage: python3 import_lists.py
"""
from pathlib import Path
import re
import unicodedata

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCES = {"concept_semantics_expanded.md": "A", "twopager.md": "B", "assumptions_table.md": "B", "framing.md": "B"}
ARXIV = re.compile(r"arxiv\.org/abs/([\w.\-/]+?)(?:v\d+)?(?=$|[\s)\]])")
DOI = re.compile(r"doi\.org/(10\.\S+?)(?=[\s)]|$)")
URL = re.compile(r"https?://\S+")
FORMAT_A = re.compile(r"^\d+\.\s+(?P<authors>.+?)\s+\((?P<year>\d{4})[a-z]?\)\.\s+(?P<rest>.+)$")
FORMAT_B = re.compile(r'^\[\d+\]\s+(?P<authors>[^"“]+?),?\s+["“](?P<title>[^"”]+)[,"”]+\s*(?P<rest>.*)$')
PARTICLES = {"van", "von", "de", "der", "den", "le", "la", "di"}


def ascii_key(s):
    return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def first_surname(authors):
    """Surname of the first author from 'Sutton, R. S. & Barto' or 'R. S. Sutton, A. G. Barto' or 'DeepSeek-AI' or 'OpenAI'."""
    first = re.split(r",\s*(?=[A-Z]\.)|\s*&\s*|,\s+|\s+and\s+|\s+et al", authors.strip())[0].strip()
    if "," in authors and re.match(r"^[A-Z][\w'’\-]+(\s[A-Z][\w'’\-]+)*,", authors):     # 'Sutton, R. S.' form
        return authors.split(",")[0].strip()
    words = [w for w in first.replace(",", " ").split() if not re.fullmatch(r"[A-ZÖÇ]\.|[A-Z]\.[A-Z]\.", w)]
    return " ".join(words[-1:]) if words else first


def short_label(authors, surname):
    n_authors = len(re.findall(r"(?:^|&|,|\band\b)\s*[A-Z][\w'’\-]+(?:,\s*[A-Z]\.)|[A-Z]\.\s*[A-Z][\w'’\-]+", authors))
    many = "et al" in authors or n_authors > 2
    two = n_authors == 2 and not many
    if two:
        others = [first_surname(p) for p in re.split(r"\s*&\s*|\s+and\s+", authors)]
        return f"{others[0]} and {others[1]}" if len(others) == 2 else surname
    return f"{surname} et~al." if many else surname


def parse(line, fmt):
    m = (FORMAT_A if fmt == "A" else FORMAT_B).match(line.strip())
    if not m:
        return None
    g = m.groupdict()
    if fmt == "A":
        year = g["year"]
        title = re.split(r"\.\s+\*|\.\s+https?://|\.\s+[A-Z]", g["rest"], 1)[0].strip(" .")
    else:
        ym = re.search(r"\b((?:19|20)\d{2})\b", g["rest"] + " " + g["authors"])
        year = ym.group(1) if ym else ""
        title = g["title"].strip()
    url = URL.search(line)
    return {"authors": g["authors"].strip(), "year": year, "title": title, "url": url.group(0).rstrip(".,;)") if url else "", "line": line.strip()}


def identifier(text):
    for pat in (ARXIV, DOI):
        m = pat.search(text)
        if m:
            return m.group(1).rstrip(".,;")
    m = URL.search(text)
    return m.group(0).rstrip(".,;") if m else text[:80]


def to_text(p):
    """Printed reference in the house style: initials-first authors, quoted title, italic venue, year, URL."""
    rest = p["line"].split(p["title"], 1)[-1] if p["title"] in p["line"] else ""
    venue = re.search(r"\*([^*]+)\*", rest)
    venue_s = f" *{venue.group(1).strip()}*," if venue else ""
    title = p["title"].strip("*")
    quoted = f'"{title},"' if title == p["title"] else f"*{title}*,"          # a book title is set in italics, not quotes
    return f'{p["authors"]}, {quoted}{venue_s} {p["year"]}. {p["url"]}'.replace(",,", ",").strip()


def main():
    old = yaml.safe_load((ROOT.parent / "paper__debunking/040_biblio/refs.yaml").read_text())
    old_by_id = {identifier(r["text"]): r for r in old}
    parsed, unparsed = {}, []
    for name, fmt in SOURCES.items():
        text = (ROOT / "900_archive/pre_pipeline" / name).read_text()
        in_refs = False
        for line in text.splitlines():
            if re.match(r"^## (References|Bibliography)", line):
                in_refs = True
                continue
            if in_refs and re.match(r"^(\d+\.|\[\d+\])\s", line):
                p = parse(line, fmt)
                if not p or not p["year"]:
                    unparsed.append(f"{name}: {line.strip()}")
                    continue
                ident = identifier(line)
                if ident in parsed:
                    continue
                parsed[ident] = p
    refs, used = [], {}
    for ident, p in parsed.items():
        if ident in old_by_id:
            r = dict(old_by_id[ident])
        else:
            surname = first_surname(p["authors"])
            base = ascii_key(surname) + p["year"]
            r = {"key": base, "short": short_label(p["authors"], surname).replace(" et al.", " et~al."), "year": p["year"], "text": to_text(p)}
        used.setdefault(r["key"], []).append(r)
        refs.append(r)
    for key, rows in used.items():                       # a/b suffixes for key collisions
        if len(rows) > 1:
            for i, r in enumerate(rows):
                r["key"] = f"{key}{'abcdefgh'[i]}"
    header = "# One entry per work. key: stable citation key used as [@key] in the draft.\n# short and year: the natbib label. text: the reference as printed.\n# Imported by import_lists.py from the archived lists on 2026-11-25; hand-edited after.\n"
    (HERE / "refs.yaml").write_text(header + yaml.safe_dump(refs, allow_unicode=True, sort_keys=False, width=1000))
    (HERE / "unparsed.txt").write_text("\n".join(unparsed) + "\n")
    print(len(refs), "refs;", len(unparsed), "unparsed;", sum(1 for r in refs if r["key"] in {o["key"] for o in old}), "reuse debunking keys")


if __name__ == "__main__":
    main()
