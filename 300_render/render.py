"""Pure rendering functions: data -> markdown or LaTeX strings. No file or process I/O here."""
import re

DIRECTIVE = re.compile(r"\{\{(\w+):(\w+)\}\}")
CITE_KEY = re.compile(r"@([a-z][a-z0-9]*[0-9][a-z]?)\b")
SHORT_CELL = 14  # a column whose cells all have at most this many visible characters gets its natural width


def expand(text, resolvers):
    """Replace every {{kind:name}} by resolvers[kind](name). Unknown kinds or names raise KeyError."""
    return DIRECTIVE.sub(lambda m: resolvers[m.group(1)](m.group(2)), text)


def cite_keys(text):
    """Keys in pandoc citation syntax (@key) in markdown."""
    return set(CITE_KEY.findall(text))


def latex_cite_keys(latex):
    """Keys in \\citep/\\citet commands in LaTeX."""
    groups = re.findall(r"\\cite[pt](?:\[[^\]]*\])?\{([^}]*)\}", latex)
    return {k.strip() for g in groups for k in g.split(",")}


def split_draft(draft):
    """Draft markdown -> (title, abstract, body, appendix). The appendix starts at the first heading labelled {#app:...}."""
    title, rest = draft.split("\n", 1)
    abstract, body = rest.split("## Abstract\n", 1)[1].split("\n## ", 1)
    body = "## " + body
    m = re.search(r"^## .*\{#app:", body, re.M)
    cut = m.start() if m else len(body)
    return title.lstrip("# ").strip(), abstract.strip(), body[:cut], body[cut:]


def visible_length(latex):
    text = re.sub(r"\\cite[pt](\[[^]]*\])?\{[^}]*\}", "(Author, 2026)", latex)
    return len(re.sub(r"\\[a-zA-Z]+\*?|[{}$]", "", text).strip())


def column_spec(columns):
    """Columns of LaTeX cells -> tabularx spec: short columns 'l', long ones ragged X."""
    wide = [max(visible_length(c) for c in col) > SHORT_CELL for col in columns]
    if not any(wide):
        wide = [True] * len(columns)
    return "@{}" + "".join(r">{\raggedright\arraybackslash}X" if w else "l" for w in wide) + "@{}"


def table_latex(caption, label, header, rows):
    """Header and rows of LaTeX cells -> a table float with tabularx."""
    columns = list(zip(header, *rows))
    lines = [" & ".join(r) + r" \\" for r in rows]
    return "\n".join([r"\begin{table}[!htb]", r"\centering\small\setlength{\tabcolsep}{3pt}",
                      rf"\caption{{{caption}}}\label{{{label}}}",
                      rf"\begin{{tabularx}}{{\textwidth}}{{{column_spec(columns)}}}", r"\toprule",
                      " & ".join(header) + r" \\", r"\midrule", *lines, r"\bottomrule",
                      r"\end{tabularx}", r"\end{table}"])


def bullet_list(items):
    return "\n".join(f"- **{head}.** {text}" for head, text in items)


def natbib_labels(refs):
    """refs [{key, short, year}] -> {key: 'Short(2024a)'}; same short label and year get a, b, ... in key order."""
    groups = {}
    for r in sorted(refs, key=lambda r: r["key"]):
        groups.setdefault((r["short"], r["year"]), []).append(r["key"])
    out = {}
    for (short, year), keys in groups.items():
        for i, k in enumerate(keys):
            out[k] = f"{short}({year}{'abcdefgh'[i] if len(keys) > 1 else ''})"
    return out


def wrap_bare_urls(text):
    return re.sub(r"(?<![<(])(https?://[^\s)>]+?)([.,;]?)(?=\s|$)", r"<\1>\2", text)
