import random
from contrasts import attribution, code_grid, contrast_problems, pair_problems, sentence_problems, shared_against, summarise

SETTINGS = [{"id": "T-RL", "phase": "training", "culture": "RL"}, {"id": "T-X", "phase": "training", "culture": "LLM"},
            {"id": "T-Y", "phase": "training", "culture": "LLM"}, {"id": "D-RL", "phase": "deployment", "culture": "RL"},
            {"id": "D-X", "phase": "deployment", "culture": "LLM"}, {"id": "D-Y", "phase": "deployment", "culture": "LLM"}]
PAIRS = [{"id": "C:T-X", "axis": "culture", "a": "T-RL", "b": "T-X"}, {"id": "C:T-Y", "axis": "culture", "a": "T-RL", "b": "T-Y"},
         {"id": "C:D-X", "axis": "culture", "a": "D-RL", "b": "D-X"}, {"id": "C:D-Y", "axis": "culture", "a": "D-RL", "b": "D-Y"},
         {"id": "P:RL", "axis": "phase", "a": "T-RL", "b": "D-RL"}, {"id": "P:X", "axis": "phase", "a": "T-X", "b": "D-X"}]
IDS = [s["id"] for s in SETTINGS]


def grid_of(prop, codes):
    return code_grid([{"property": prop, "setting": s, "code": c} for s, c in zip(IDS, codes)])


def test_the_original_error_is_attributed_to_phase_not_culture():
    # reward used for learning: yes in training, no in deployment, for RL and LLM alike
    g = grid_of("R2", ["yes", "yes", "yes", "no", "no", "no"])
    a = attribution(g, "R2", PAIRS, SETTINGS)
    assert a["label"] == "phase" and a["culture_deployment"] == "none" and a["phase_RL"] == "yes"


def test_a_real_culture_difference_in_both_phases():
    g = grid_of("O1", ["no", "yes", "yes", "no", "yes", "yes"])
    a = attribution(g, "O1", PAIRS, SETTINGS)
    assert a["label"] == "culture" and a["culture_training"] == "all" and a["culture_deployment"] == "all"


def test_sentence_comparing_rl_training_with_llm_deployment_is_a_phase_confound():
    g = grid_of("R2", ["yes", "yes", "yes", "no", "no", "no"])
    out = sentence_problems({"a": ["T-RL"], "b": ["D-X", "D-Y"], "property": "R2"}, g, SETTINGS)
    assert any("phase confound" in p for p in out)


def test_sentence_one_sided_difference_the_rl_setting_shares_fails():
    g = grid_of("R2", ["yes", "yes", "yes", "no", "no", "no"])
    out = sentence_problems({"a": ["D-RL"], "b": ["D-X", "D-Y"], "property": "R2"}, g, SETTINGS)
    assert any("share code" in p for p in out)


def test_sentence_matched_true_difference_passes():
    g = grid_of("R1", ["yes", "yes", "yes", "yes", "no", "no"])
    assert sentence_problems({"a": ["D-RL"], "b": ["D-X", "D-Y"], "property": "R1"}, g, SETTINGS) == []


def test_unregistered_contrast_fails():
    assert sentence_problems({"a": ["D-RL"], "b": ["D-X"], "property": None}, {}, SETTINGS)[0].startswith("unregistered")


def test_contrast_claims_checked_against_codes():
    g = grid_of("R2", ["yes", "yes", "yes", "no", "no", "no"])
    claims = [{"id": "c1", "kind": "contrast", "property": "R2", "axis": "culture", "phase": "deployment", "extent": "all"},
              {"id": "c2", "kind": "contrast", "property": "R2", "axis": "phase", "culture": "RL", "phase": "", "extent": ""}]
    out = contrast_problems(claims, g, PAIRS, SETTINGS, [{"id": "R2"}])
    assert len(out) == 1 and "c1" in out[0]


def test_pairs_must_be_minimal():
    bad = [{"id": "x", "axis": "culture", "a": "T-RL", "b": "D-X"}]
    assert pair_problems(bad, SETTINGS) == ["pair x: a culture pair must hold phase fixed and differ in culture"]
    assert pair_problems(PAIRS, SETTINGS) == []


def test_property_no_cross_phase_culture_attribution_randomised():
    """For any coding: culture attribution at a phase implies a same-phase culture pair differs; phase-only
    differences never yield a culture attribution."""
    rnd = random.Random(15)
    for _ in range(500):
        codes = [rnd.choice(["yes", "no", "partly"]) for _ in IDS]
        g = grid_of("P", codes)
        a = attribution(g, "P", PAIRS, SETTINGS)
        for ph, prefix in (("training", "T-"), ("deployment", "D-")):
            rl = g[("P", f"{prefix}RL")]
            llm = [g[("P", s)] for s in IDS if s.startswith(prefix) and "RL" not in s]
            assert (a[f"culture_{ph}"] != "none") == any(c != rl for c in llm)
        # a pure phase pattern is never called culture
        t, d = rnd.choice(["yes", "no"]), rnd.choice(["yes", "no"])
        pure = grid_of("Q", [t, t, t, d, d, d])
        assert "culture" not in attribution(pure, "Q", PAIRS, SETTINGS)["label"]


def test_summarise():
    g = grid_of("O1", ["no", "yes", "yes", "no", "yes", "partly"])
    assert summarise(g, "O1", ["T-X", "T-Y"]) == "yes"
    assert summarise(g, "O1", ["D-X", "D-Y"]) == "partly: D-Y; yes: D-X"


def test_phase_only_claim_fails_when_culture_also_differs():
    g = grid_of("R1", ["yes", "yes", "yes", "yes", "no", "no"])
    claim = [{"id": "c", "kind": "contrast", "property": "R1", "axis": "phase", "culture": "LLM", "phase": "", "extent": "only"}]
    assert any("phase only" in x for x in contrast_problems(claim, g, PAIRS, SETTINGS, [{"id": "R1"}]))


def test_same_claim_passes_when_codes_match_and_fails_when_they_differ():
    g = grid_of("P1", ["yes", "yes", "yes", "no", "no", "no"])
    ok = {"a": ["D-RL"], "b": ["D-X"], "property": "P1", "relation": "same"}
    assert sentence_problems(ok, g, SETTINGS) == []
    bad = {"a": ["T-RL"], "b": ["D-X"], "property": "P1", "relation": "same"}
    assert any("not the same" in p for p in sentence_problems(bad, g, SETTINGS))


def test_general_and_within_group_claims_are_not_checked_here():
    assert sentence_problems({"a": ["D-X"], "b": [], "property": None, "relation": "general"}, {}, SETTINGS) == []
    assert sentence_problems({"a": ["T-X", "T-Y"], "b": [], "property": None, "relation": "varies_within"}, {}, SETTINGS) == []


def test_shared_against_keeps_properties_the_rivals_do_not_share():
    codes = [{"property": p, "setting": s, "code": c} for p, row in
             {"P": ["yes", "yes", "no"], "Q": ["yes", "yes", "yes"], "R": ["partly", "yes", "yes"], "S": ["no", "no", "yes"]}.items()
             for s, c in zip(["REF", "X", "Y"], row)]
    g = code_grid(codes)
    assert shared_against(g, ["P", "Q", "R", "S"], "X", "REF", ["Y"]) == ["P", "S"]


def test_phase_claim_fails_within_a_culture_that_shares_the_code():
    # "deployment has no reward function": true for the LLM settings, false for D-RL
    g = grid_of("R1", ["yes", "yes", "yes", "yes", "no", "no"])
    out = sentence_problems({"a": ["D-RL", "D-X", "D-Y"], "b": ["T-RL", "T-X", "T-Y"], "property": "R1"}, g, SETTINGS)
    assert any("within RL" in p for p in out)
    ok = sentence_problems({"a": ["D-X", "D-Y"], "b": ["T-X", "T-Y"], "property": "R1"}, g, SETTINGS)
    assert ok == []


def test_unhedged_difference_on_a_partly_code_fails():
    g = grid_of("E1", ["yes", "yes", "yes", "partly", "no", "no"])
    claim = {"a": ["D-RL"], "b": ["D-X", "D-Y"], "property": "E1", "relation": "differ"}
    assert any("partly" in p for p in sentence_problems(claim, g, SETTINGS))
    assert sentence_problems({**claim, "hedged": True}, g, SETTINGS) == []


def test_differ_on_allows_partly_but_not_shared_codes():
    # "the settings differ on whether X" says the codes differ, not which side has X
    g = grid_of("E1", ["yes", "yes", "yes", "partly", "no", "no"])
    claim = {"a": ["D-RL"], "b": ["D-X", "D-Y"], "property": "E1", "relation": "differ_on"}
    assert sentence_problems(claim, g, SETTINGS) == []
    g2 = grid_of("E1", ["yes", "yes", "yes", "no", "no", "no"])
    assert any("share code" in p for p in sentence_problems(claim, g2, SETTINGS))
