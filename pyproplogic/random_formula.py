from pyproplogic import LogicFormula


def random_formula(n: int, atom_list=None) -> LogicFormula:
    """
    Returns a LogicFormula made of random operators and atoms.

    Paramteres
    ----------
    n: int
        The height of the formula's parse tree.

    atom_list: list[str], optional
        A list of atom names to be picked. Default value is [P - Z].

    """
    import random

    if n == 1:
        return LogicFormula.atom(
            random.choice(
                atom_list if atom_list else [chr(ord("P") + x) for x in range(11)]
            )
        )
    operator = random.choice(("~", "&", "|", "->", "<->"))
    if operator == "~":
        return random_formula(n - 1, atom_list).negation()
    return LogicFormula(
        operator,
        random_formula(n // 2, atom_list),
        random_formula(n - n // 2, atom_list),
    )
