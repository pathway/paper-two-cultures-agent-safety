import pytest
import checks
import render


def test_expand_resolves_and_rejects_unknown():
    assert render.expand("a {{fact:x}} b", {"fact": {"x": "1"}.__getitem__}) == "a 1 b"
    with pytest.raises(KeyError):
        render.expand("{{fact:y}}", {"fact": {"x": "1"}.__getitem__})


def test_split_draft():
    d = "# T\n\n## Abstract\n\nA.\n\n## Intro {#sec:intro}\n\nB.\n\n## Reasons {#app:cells}\n\nC.\n"
    title, abstract, body, app = render.split_draft(d)
    assert (title, abstract) == ("T", "A.")
    assert body.startswith("## Intro") and "C." not in body and app.startswith("## Reasons")


def test_cite_keys_markdown_and_latex():
    assert render.cite_keys("x [@sutton2018; @mclean2026, {§3}] and @breiman2001") == {"sutton2018", "mclean2026", "breiman2001"}
    assert render.latex_cite_keys(r"\citep[§3]{a2020, b2021} \citet{c2022}") == {"a2020", "b2021", "c2022"}


def test_natbib_labels_disambiguate_same_label_and_year():
    refs = [{"key": "yao2023a", "short": "Yao et~al.", "year": "2023"}, {"key": "yao2023b", "short": "Yao et~al.", "year": "2023"},
            {"key": "altman1999", "short": "Altman", "year": "1999"}]
    assert render.natbib_labels(refs) == {"yao2023a": "Yao et~al.(2023a)", "yao2023b": "Yao et~al.(2023b)", "altman1999": "Altman(1999)"}


def test_cell_problems_missing_value_and_quote_rules():
    prims = [{"id": "reward"}]
    settings = [{"id": "A"}, {"id": "B"}]
    cells = [{"primitive": "reward", "setting": "A", "value": "", "reason": 'says "x y"', "evidence_type": "judgement", "evidence": "", "evidence_source": ""}]
    out = checks.cell_problems(prims, settings, cells)
    assert "cell reward B: missing" in out and "cell reward A: no value" in out
    assert any("judgement cell that quotes" in p for p in out)
    good = [{"primitive": "reward", "setting": "A", "value": "v", "reason": 'says "x y"', "evidence_type": "quote", "evidence": "e1", "evidence_source": "k"},
            {"primitive": "reward", "setting": "B", "value": "v", "reason": "r", "evidence_type": "judgement", "evidence": "", "evidence_source": ""}]
    assert checks.cell_problems(prims, settings, good) == []


def test_settings_and_primitive_problems():
    assert checks.settings_problems([{"id": "X", "phase": "nope", "posed_as": "", "decision": "D9"}], [{"id": "D3"}]) == [
        "setting X: phase must be training or deployment", "setting X: no 'posed as'", "setting X: decision 'D9' is not in 005_decisions"]
    assert checks.primitive_problems([{"id": "reward", "rl_definition": "r", "evidence": "e1; e9"}], [{"id": "e1"}]) == [
        "primitive reward: evidence e9 is not a sutton2018 extract"]


def test_incident_and_label_problems():
    inc = [{"id": "C1", "setting": "deployed-incident", "verification": "verified-primary", "assumption_tags": "A1,Z9",
            "source_urls": "https://x.test/a", "snapshot_note": ""}]
    snaps = [{"incident": "C1", "url": "https://x.test/a", "status": "unavailable"}]
    out = checks.incident_problems(inc, [{"id": "A1"}], snaps)
    assert "incident C1: unknown assumption tag Z9" in out and any("snapshot_note" in p for p in out)
    labels = [{"incident": "C1", "rater": "haiku", "dimension": "writable_in_advance", "value": "maybe"}]
    out = checks.label_problems(inc, labels, raters=("haiku",))
    assert "label C1 haiku writable_in_advance: bad value 'maybe'" in out and "label C1 haiku failure_type: missing" in out


def test_typed_count_and_draft_table_rows():
    assert checks.typed_count_problems("we read 70 incidents", ["incidents"]) == ['draft: typed count "70 ... incidents"; use a {{fact:...}} so the count follows its set']
    assert checks.typed_count_problems("the {{fact:incidents_n}} incidents", ["incidents"]) == []
    assert checks.draft_problems("text\n| a | b |\n") == ["draft line 2: typed table row; import tables with {{table:...}}"]


def test_missing_keys_and_verified_quotes():
    assert checks.missing_keys(["see @nope2020"], [{"key": "yes2020"}]) == ["citation @nope2020 not in 040_biblio"]
    assert checks.verified_quotes('x\n\nVerified quotes\n- "a b"\n- "c"\n') == ["a b", "c"]
