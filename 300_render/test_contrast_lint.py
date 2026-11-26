import contrast_lint as cl

SETTINGS = [{"id": "D-RL", "phase": "deployment", "culture": "RL", "label": "RL agent, deployment", "posed_as": "fixed policy"}]
PROPS = [{"id": "R1", "question": "Is a reward function defined for the task?"}]


def test_lint_uses_port_and_caches():
    calls = []
    def fake(prompt):
        calls.append(prompt)
        return '[{"span": "no reward", "a": ["D-RL"], "b": ["D-X"], "property": "R1", "implicit": true}]'
    cache = cl.lint(["P one."], SETTINGS, PROPS, {}, fake)
    assert len(calls) == 1 and "D-RL: deployment, RL" in calls[0]
    [entry] = cache.values()
    assert entry["claims"][0]["property"] == "R1" and entry["claims"][0]["implicit"] is True
    cl.lint(["P one."], SETTINGS, PROPS, cache, fake)
    assert len(calls) == 1                         # cached: no second call


def test_malformed_answer_is_recorded_not_raised():
    cache = cl.lint(["P two."], SETTINGS, PROPS, {}, lambda p: "not json")
    assert "error" in next(iter(cache.values()))


def test_parse_strips_fences():
    assert cl.parse('```json\n[]\n```') == []


def test_parse_tolerates_prose_after_json_and_null_groups():
    out = cl.parse('Here:\n[{"span": "x", "a": null, "b": ["D-RL"], "property": "R1"}]\nThat is all.')
    assert out == [{"span": "x", "a": [], "b": ["D-RL"], "property": "R1", "relation": "differ", "implicit": False, "hedged": False}]


def test_empty_answer_is_an_error():
    import pytest
    with pytest.raises(ValueError):
        cl.parse("")


def test_cache_is_saved_after_each_paragraph():
    saved = []
    cl.lint(["P a.", "P b."], SETTINGS, PROPS, {}, lambda p: "[]", save=lambda c: saved.append(len(c)))
    assert saved == [1, 2]


def test_parse_keeps_known_relations_only():
    assert cl.parse('[{"span": "x", "a": [], "b": [], "property": null, "relation": "general"}]')[0]["relation"] == "general"
    assert cl.parse('[{"span": "x", "a": [], "b": [], "property": null, "relation": "odd"}]')[0]["relation"] == "differ"


def test_adjudicate_only_failing_claims_and_cache_verdicts():
    cache = {"h": {"paragraph": "P.", "claims": [{"span": "s1", "a": ["D-RL"], "b": [], "property": None, "relation": "differ"},
                                                  {"span": "s2", "a": [], "b": [], "property": None, "relation": "general"}]}}
    calls = []
    def ask(prompt):
        calls.append(prompt)
        return '{"verdict": "mapping_error", "claim": {"span": "s1", "a": [], "b": [], "property": null, "relation": "general"}, "reason": "framing"}'
    failing = lambda c: c["relation"] == "differ"
    cl.adjudicate(cache, failing, lambda c: "codes", ask)
    adj = cache["h"]["claims"][0]["adjudication"]
    assert adj["verdict"] == "mapping_error" and adj["claims"][0]["relation"] == "general" and len(calls) == 1
    cl.adjudicate(cache, failing, lambda c: "codes", ask)
    assert len(calls) == 1                         # cached


def test_effective_claim_uses_adjudicated_mapping():
    c = {"span": "s", "a": ["D-RL"], "b": [], "property": None, "relation": "differ",
         "adjudication": {"verdict": "mapping_error", "claims": [{"span": "s", "a": [], "b": [], "property": None, "relation": "general"}]}}
    assert cl.effective(c)[0]["relation"] == "general"
    c["adjudication"]["verdict"] = "real"
    assert cl.effective(c)[0]["relation"] == "differ"


def test_adjudicate_reads_only_current_paragraphs():
    # stale entries (an older prompt version) may lack fields; they must not be read
    cache = {"old": {"paragraph": "Old.", "claims": [{"span": "x", "a": [], "b": []}]},
             "new": {"paragraph": "New.", "claims": [{"span": "s", "a": ["D-RL"], "b": [], "property": None, "relation": "differ"}]}}
    ask = lambda p: '{"verdict": "real", "claim": null, "reason": "r"}'
    cl.adjudicate(cache, lambda c: "bad", lambda c: "codes", ask, current={"new"})
    assert "adjudication" not in cache["old"]["claims"][0]
    assert cache["new"]["claims"][0]["adjudication"]["verdict"] == "real"


def test_adjudicate_saves_after_each_verdict():
    cache = {"h": {"paragraph": "P.", "claims": [{"span": s, "a": [], "b": [], "property": None, "relation": "differ"} for s in "ab"]}}
    saves = []
    cl.adjudicate(cache, lambda c: "bad", lambda c: "codes", lambda p: '{"verdict": "real", "claim": null, "reason": "r"}',
                  current={"h"}, save=lambda c: saves.append(1))
    assert len(saves) == 2


def test_parse_splits_a_claim_over_several_properties():
    out = cl.parse('[{"span": "s", "a": ["D-CHAT"], "b": ["D-RL"], "property": ["R1", "E1"], "relation": "differ"}]')
    assert [c["property"] for c in out] == ["R1", "E1"]


def test_effective_is_a_list_and_empty_when_adjudicator_finds_no_claim():
    raw = {"span": "s", "a": ["D-RL"], "b": [], "property": None, "relation": "differ"}
    assert cl.effective(raw) == [raw]
    raw["adjudication"] = {"verdict": "mapping_error", "claims": []}
    assert cl.effective(raw) == []


def test_adjudicate_accepts_one_claim_a_list_or_null():
    for answer, n in [('{"verdict": "mapping_error", "claim": null, "reason": "r"}', 0),
                      ('{"verdict": "mapping_error", "claim": {"span": "s", "property": ["R1", "E1"]}, "reason": "r"}', 2),
                      ('{"verdict": "mapping_error", "claim": [{"span": "s"}, {"span": "t"}], "reason": "r"}', 2)]:
        cache = {"h": {"paragraph": "P.", "claims": [{"span": "s", "a": [], "b": [], "property": None, "relation": "differ"}]}}
        cl.adjudicate(cache, lambda c: "bad", lambda c: "codes", lambda p: answer, current={"h"})
        assert len(cl.effective(cache["h"]["claims"][0])) == n


def test_parse_keeps_hedged_and_defaults_to_false():
    out = cl.parse('[{"span": "s", "property": "E1", "hedged": true}, {"span": "t", "property": "E1"}]')
    assert [c["hedged"] for c in out] == [True, False]


def test_parse_keeps_differ_on():
    assert cl.parse('[{"span": "s", "property": "E1", "relation": "differ_on"}]')[0]["relation"] == "differ_on"


def test_corrected_claim_inherits_hedged_when_the_adjudicator_omits_it():
    cache = {"h": {"paragraph": "P.", "claims": [{"span": "s", "a": [], "b": [], "property": "O2", "relation": "differ", "hedged": True}]}}
    answer = '{"verdict": "mapping_error", "claim": {"span": "s", "a": ["T-X"], "b": ["D-X"], "property": "O2", "relation": "differ"}, "reason": "r"}'
    cl.adjudicate(cache, lambda c: "bad", lambda c: "codes", lambda p: answer, current={"h"})
    assert cl.effective(cache["h"]["claims"][0])[0]["hedged"] is True


def test_span_key_ignores_trailing_punctuation():
    # round 4: the extractor returned an overridden span without its final full stop, and the override stopped matching
    assert cl.span_key("they differ by whether a human sees each step.") == cl.span_key("they differ by whether a human sees each step")
    assert cl.span_key("  a claim; ") == "a claim"
    assert cl.span_key("a claim") != cl.span_key("another claim")
