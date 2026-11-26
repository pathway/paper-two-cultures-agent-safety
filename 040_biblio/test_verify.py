import verify

REF = 'A. Wachi, W. Hashimoto, "Safe Exploration in Reinforcement Learning: A Generalized Formulation and Algorithms," *NeurIPS 2023*. https://arxiv.org/abs/2310.03225'


def test_identifier_and_title():
    assert verify.identifier(REF) == ("arxiv", "2310.03225")
    assert verify.identifier("X, *Book*, 1999. https://doi.org/10.1201/9781315140223") == ("doi", "10.1201/9781315140223")
    assert verify.identifier("X, a blog post. https://example.org/post.") == ("url", "https://example.org/post")
    assert verify.identifier("X, *Journal*. https://doi.org/10.1016/S0004-3702(98)00023-X") == ("doi", "10.1016/S0004-3702(98)00023-X")
    assert verify.identifier("D. E. Kirk, *Optimal Control Theory*, 1970.") == (None, None)
    assert verify.cited_title(REF).startswith("Safe Exploration in Reinforcement Learning")


def test_judge():
    assert verify.judge(REF, "Safe Exploration in Reinforcement Learning: A Generalized Formulation and Algorithms", "Akifumi Wachi") == "ok"
    assert verify.judge(REF, "Attention Is All You Need", "Ashish Vaswani") == "mismatch"
    assert verify.judge(REF, "", "") == "not_found"


def test_judge_page():
    assert verify.judge_page(REF, "... Safe Exploration in Reinforcement Learning: A Generalized Formulation and Algorithms ...") == "ok"
    assert verify.judge_page(REF, "") == "unverified"
