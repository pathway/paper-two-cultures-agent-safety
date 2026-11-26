import json
import scan

TEXT = "Intro text.\n\nAssumption 3.1 (Stationarity). The MDP is ergodic\nfor any policy.\n\nTheorem 4.1. Safety holds.\n\nMore text."


def test_structural_finds_numbered_statements():
    found = scan.structural(TEXT)
    assert [(f["topic"], f["locator"]) for f in found] == [("assumption", "Assumption 3.1"), ("guarantee", "Theorem 4.1")]
    assert found[0]["text"] == "Assumption 3.1 (Stationarity). The MDP is ergodic for any policy."


def test_llm_pass_keeps_only_verbatim_passages():
    answer = json.dumps([{"topic": "reset", "locator": "", "text": "The MDP is ergodic for any policy."},
                         {"topic": "reset", "locator": "", "text": "The MDP is never reset."}])
    rows = scan.verified(scan.llm(TEXT, "protocol", lambda prompt: answer), TEXT, "llm")
    assert [(r["line"], r["text"]) for r in rows] == [(3, "The MDP is ergodic for any policy.")]


def test_llm_pass_survives_a_malformed_answer():
    assert scan.llm(TEXT, "protocol", lambda prompt: "not json") == []


def test_parse_proposals_tolerates_bad_files():
    assert scan.parse_proposals("not json") == [] and scan.parse_proposals('{"a": 1}') == []
    assert scan.parse_proposals('[{"topic": "reset", "text": "x"}, 3]') == [{"topic": "reset", "locator": "", "text": "x"}]
