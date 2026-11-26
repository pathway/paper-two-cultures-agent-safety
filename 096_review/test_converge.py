import pytest
from converge import summarise


def row(v, changed="no"):
    return {"verdict": v, "changed": changed}


def test_round_with_all_supported_and_no_change_is_clean():
    [s] = summarise([("round_1", {"K01": row("supported"), "K02": row("supported")})])
    assert s["clean"] and s["not_supported"] == [] and s["flips"] == []


def test_a_changed_claim_makes_a_round_not_clean_even_if_supported():
    [s] = summarise([("round_1", {"K01": row("supported", "yes")})])
    assert not s["clean"] and s["changed"] == ["K01"]


def test_an_accepted_finder_hit_makes_a_round_not_clean():
    [s] = summarise([("round_1", {"K01": {"verdict": "supported", "changed": "no", "finder_hits": "2"}})])
    assert not s["clean"] and s["hits"] == 2


def test_flips_compare_verdicts_with_the_previous_round():
    r1 = {"K01": row("qualify"), "K02": row("supported")}
    r2 = {"K01": row("supported"), "K02": row("supported")}
    s1, s2 = summarise([("round_1", r1), ("round_2", r2)])
    assert s1["not_supported"] == ["K01"] and s2["flips"] == ["K01"] and s2["clean"]
