# PyPropLogic

> **Note: this project is still in early development, and many of its features are not yet available.**

PyPropLogic is a Python library for parsing, manipulating, and visualizing propositional
logic. It provides a set of tools to build and manipulate propositional formulas, and to
perform logical operations on them.

---

## Installation

To install the module, clone the repository to your local machine and run the following
command in the root directory of the cloned repository:
```
python setup.py install
```
Alternatively, you can install the library in development mode by running:
```
python setup.py develop
```

---

## Usage

Here are some examples of how to use this module:

```python
import pyproplogic as ppl
from pyproplogic.common import P, Q, IMPLICATION

# Creating propositional formulas
R = ppl.atom("R")
formula = P & (Q >> R)
random = ppl.random_formula(5)

# Evaluating propositional formulas
valuation = {P: True, Q: False, R: True}
result = formula.eval(valuation)  # True
truth_table = formula.get_truth_table()
tautology = IMPLICATION.is_tautology()

# Simplifying propositional formulas
formula = ((P & True) | False) >> Q
simplified = formula.simplify()  # Equivalent to "P"

# Converting propositional formulas to CNF and DNF
cnf = formula.to_cnf()
dnf = formula.to_dnf()

# Visualizing propositional formulas
latex_formula = formula.to_latex()
tikz_parse_tree = formula.to_latex_tikz()
```

---

## License

PyPropLogic is under the MIT license.
