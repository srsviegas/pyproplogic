from pyproplogic.commonformulas import PHI, PSI, CHI

DOUBLE_NEGATION = (~~PHI) == (PHI)

IDEMPOTENT_AND = (PHI & PHI) == (PHI)
IDEMPOTENT_OR = (PHI | PHI) == (PHI)

COMMUTATIVE_AND = (PHI & PSI) == (PSI & PHI)
COMMUTATIVE_OR = (PHI | PSI) == (PSI | PHI)

ASSOCIATIVE_AND = ((PHI & PSI) & CHI) == (PHI & (PSI & CHI))
ASSOCIATIVE_OR = ((PHI | PSI) | CHI) == (PHI | (PSI | CHI))

DISTRIBUTIVE_1 = (PHI & (PSI | CHI)) == ((PHI & PSI) | (PHI & CHI))
DISTRIBUTIVE_2 = (PHI | (PSI & CHI)) == ((PHI | PSI) & (PHI | CHI))

DE_MORGAN_AND = (~(PHI & PSI)) == (~PHI | ~PSI)
DE_MORGAN_OR = (~(PHI | PSI)) == (~PHI & ~PSI)

ABSORPTION_1 = (PHI & (PHI | PSI)) == (PHI)
ABSORPTION_2 = (PHI | (PHI & PSI)) == (PHI)

IMPLICATION = (PHI >> PSI) == (~PHI | PSI)
