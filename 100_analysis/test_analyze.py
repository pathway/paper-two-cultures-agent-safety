import math
from analyze import census_facts, classes, count_phrase, differing, fits_mclean, grid, join, kappa, pct, revised_codes, settings_where, share, wilson, pct_ci, tag_share


def test_grid_and_differing():
    g = grid([{"primitive": "reward", "setting": "A", "value": "scalar"}, {"primitive": "reward", "setting": "B", "value": "none"},
              {"primitive": "policy", "setting": "A", "value": "pi"}, {"primitive": "policy", "setting": "B", "value": "pi"}])
    assert differing(g, "A", "B", ["reward", "policy"]) == ["reward"]
    assert settings_where(g, "reward", ["A", "B"], "none") == ["B"]


def test_count_and_join():
    assert count_phrase(3, 3) == "all three" and count_phrase(1, 3) == "one of three" and count_phrase(2, 2) == "both"
    assert join([]) == "none" and join(["a"]) == "a" and join(["a", "b", "c"]) == "a, b and c"


def test_classes_and_mclean_fit():
    assert classes("['injection/untrusted-input', 'misspecification']") == ["injection/untrusted-input", "misspecification"]
    assert classes("plain") == ["plain"] and classes("") == []
    assert fits_mclean("['misspecification']") and not fits_mclean("['injection/untrusted-input', 'other']")


def test_kappa_perfect_and_chance():
    a = {"1": "x", "2": "y", "3": "x", "4": "y"}
    assert kappa(a, a) == 1.0
    b = {"1": "x", "2": "x", "3": "y", "4": "y"}
    assert abs(kappa(a, b)) < 1e-9          # agreement equals chance
    assert math.isnan(kappa({}, {}))


def test_wilson_and_pct():
    lo, hi = wilson(46, 100)
    assert 36 <= lo <= 37 and 55 <= hi <= 56
    assert pct(1, 3) == "33%" and pct(0, 0) == "n/a"
    assert pct_ci(0, 49).startswith("0% (0–")


def test_tag_share():
    inc = [{"assumption_tags": "A2,C4,D1"}, {"assumption_tags": "C4"}, {"assumption_tags": ""}]
    assert tag_share(inc, "C4") == (2, 3) and tag_share(inc, "A2") == (1, 3)


def test_share_never_prints_a_nonzero_share_as_zero():
    # round 3 (F3.16, F3.17, F3.29): 2 of 1117 papers printed as "0%" under a row labelled "at all"
    assert share(2, 1117) == "0.2%" and share(35, 703) == "5.0%"
    assert share(0, 1117) == "0%" and share(0, 0) == "n/a"
    assert share(1, 100000) == "<0.1%"
    assert all(share(k, n) not in ("0%", "0.0%") for n in (7, 1117, 99999) for k in (1, 2, 5))


def test_census_facts_papers_citing_other_corpus():
    side = lambda own, other, k, n: {"frac_to_A": own, "frac_to_B": other, "papers_citing_A": k, "papers_citing_B": k, "papers": n}
    m = {"sizes": {"A": 1250, "B": 570, "bridge": 3}, "cross_citation": {"A": side(0.065, 0.0001, 2, 1117), "B": side(0.0022, 0.02, 35, 703)}}
    f = census_facts(m)
    assert f["a_papers_citing_b"] == "0.2%" and f["a_papers_citing_b_n"] == "2"
    assert f["b_papers_citing_a"] == "5.0%" and f["b_papers_citing_a_n"] == "35"


def test_revised_codes_counts_codes_set_in_review():
    # round 4: the paper says how many codes a review round changed after the raters and the adjudicator
    codes = [{"by": "LLM (two independent Sonnet raters agree)"}, {"by": "LLM (adjudicated; A=no, B=partly)"},
             {"by": "LLM (two independent Sonnet raters agree); reason or sources edited by gate round 3 (fixer), code unchanged"},
             {"by": "gate round 3 (fixer)"}, {"by": "gate round 4 (fixer); rater columns kept (partly, partly)"}]
    assert revised_codes(codes) == 2 and revised_codes([]) == 0
