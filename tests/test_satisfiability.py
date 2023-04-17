from pyproplogic.commonformulas import P, Q, R, DE_MORGAN_AND, IMPLICATION


def test_is_tautology():
    assert (P | ~P).is_tautology()
    assert ((P & Q) >> P).is_tautology()
    assert not (P & Q).is_tautology()
    assert not (P).is_tautology()


def test_is_contradiction():
    assert (P & ~P).is_contradiction()
    assert not ((P & Q) >> (R & ~R)).is_contradiction()
    assert not (P | Q).is_contradiction()
    assert not (P).is_contradiction()


def test_is_satisfiable():
    assert (P & Q).is_satisfiable()
    assert (P | ~P).is_satisfiable()
    assert (P >> Q).is_satisfiable()
    assert not (P & ~P).is_satisfiable()


def test_is_falsifiable():
    assert (P & Q).is_falsifiable()
    assert not (P | ~P).is_falsifiable()
    assert (P >> Q).is_falsifiable()
    assert (P & ~P).is_falsifiable()


def test_satisfiable_valuations():
    valuations = [
        set(tuple(v.values()) for v in f.get_satisfiable_valuations())
        for f in (P & Q, P | ~P, P >> Q, P >> ~P)
    ]
    assert valuations[0] == {(True, True)}
    assert valuations[1] == {(True,), (False,)}
    assert valuations[2] == {(True, True), (False, True), (False, False)}
    assert valuations[3] == {(False,)}


def test_falsifiable_valuations():
    valuations = [
        set(tuple(v.values()) for v in f.get_falsifiable_valuations())
        for f in (P & Q, P | ~P, P >> Q, P >> ~P)
    ]
    assert valuations[0] == {(True, False), (False, True), (False, False)}
    assert not valuations[1]
    assert valuations[2] == {(True, False)}
    assert valuations[3] == {(True,)}


def test_is_equivalent():
    assert DE_MORGAN_AND.is_equivalent(IMPLICATION)
    assert IMPLICATION.components()[0].is_equivalent(IMPLICATION.components()[1])
    assert (P == Q).is_equivalent((P >> Q) & (Q >> P))
    assert P.is_equivalent(P)
    assert P.is_equivalent(P & (Q >> Q))
    assert not P.is_equivalent(P | Q)
    assert not P.is_equivalent(Q)
    assert not (P | Q).is_equivalent(P)
