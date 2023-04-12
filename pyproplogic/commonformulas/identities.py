from pyproplogic import LogicFormula
from atoms import PHI, PSI, CHI

DOUBLE_NEGATION = (~~PHI).biconditional(PHI)

IDEMPOTENT_AND = (PHI & PHI).biconditional(PHI)
IDEMPOTENT_OR = (PHI | PHI).biconditional(PHI)

COMMUTATIVE_AND = (PHI & PSI).biconditional(PSI & PHI)
COMMUTATIVE_OR = (PHI | PSI).biconditional(PSI | PHI)

ASSOCIATIVE_AND = ((PHI & PSI) & CHI).biconditional(PHI & (PSI & CHI))
ASSOCIATIVE_OR = ((PHI | PSI) | CHI).biconditional(PHI | (PSI | CHI))

DISTRIBUTIVE_1 = (PHI & (PSI | CHI)).biconditional((PHI & PSI) | (PHI & CHI))
DISTRIBUTIVE_2 = (PHI | (PSI & CHI)).biconditional((PHI | PSI) & (PHI | CHI))

DE_MORGAN_AND = (~(PHI & PSI)).biconditional(~PHI | ~PSI)
DE_MORGAN_OR = (~(PHI | PSI)).biconditional(~PHI & ~PSI)

ABSORPTION_1 = (PHI & (PHI | PSI)).biconditional(PHI)
ABSORPTION_2 = (PHI | (PHI & PSI)).biconditional(PHI)

IMPLICATION = (PHI >> PSI).biconditional(~PHI | PSI)