from pyproplogic.commonformulas import P, Q, R, S, T


def test_evaluate_conjunction():
    formula = P.conjunction(Q)
    assert formula.evaluate({"P": True, "Q": True}) == True
    assert formula.evaluate({"P": True, "Q": False}) == False
    assert formula.evaluate({"P": False, "Q": True}) == False
    assert formula.evaluate({"P": False, "Q": False}) == False


def test_evaluate_disjunction():
    formula = P.disjunction(Q)
    assert formula.evaluate({"P": True, "Q": True}) == True
    assert formula.evaluate({"P": True, "Q": False}) == True
    assert formula.evaluate({"P": False, "Q": True}) == True
    assert formula.evaluate({"P": False, "Q": False}) == False


def test_evaluate_negation():
    formula = P.negation()
    assert formula.evaluate({"P": True}) == False
    assert formula.evaluate({"P": False}) == True


def test_evaluate_implication():
    formula = P.implication(Q)
    assert formula.evaluate({"P": True, "Q": True}) == True
    assert formula.evaluate({"P": True, "Q": False}) == False
    assert formula.evaluate({"P": False, "Q": True}) == True
    assert formula.evaluate({"P": False, "Q": False}) == True


def test_evaluate_biconditional():
    formula = P == (Q)
    assert formula.evaluate({"P": True, "Q": True}) == True
    assert formula.evaluate({"P": True, "Q": False}) == False
    assert formula.evaluate({"P": False, "Q": True}) == False
    assert formula.evaluate({"P": False, "Q": False}) == True


def test_evaluate_complex_formulas():
    formula1 = ((P & Q) | R) >> (S == ~T)
    assert (
        formula1.evaluate({"P": True, "Q": False, "R": True, "S": False, "T": True})
        == True
    )
    assert (
        formula1.evaluate({"P": False, "Q": True, "R": False, "S": True, "T": False})
        == True
    )
    assert (
        formula1.evaluate({"P": True, "Q": True, "R": False, "S": True, "T": False})
        == True
    )

    formula2 = ~(P & (Q | R)) | (S & T)
    assert (
        formula2.evaluate({"P": True, "Q": True, "R": False, "S": False, "T": True})
        == False
    )
    assert (
        formula2.evaluate({"P": False, "Q": False, "R": True, "S": True, "T": False})
        == True
    )
    assert (
        formula2.evaluate({"P": True, "Q": False, "R": True, "S": True, "T": False})
        == False
    )

    formula3 = (P & Q & R) | (~P & ~Q & ~R)
    assert formula3.evaluate({"P": True, "Q": True, "R": True}) == True
    assert formula3.evaluate({"P": False, "Q": False, "R": False}) == True
    assert formula3.evaluate({"P": True, "Q": False, "R": True}) == False

    formula4 = (P >> Q) >> (Q >> R) >> (R >> S) >> (S >> T)
    assert (
        formula4.evaluate({"P": True, "Q": True, "R": True, "S": True, "T": True})
        == True
    )
    assert (
        formula4.evaluate({"P": False, "Q": True, "R": False, "S": True, "T": False})
        == False
    )
    assert (
        formula4.evaluate({"P": True, "Q": False, "R": True, "S": False, "T": True})
        == True
    )
