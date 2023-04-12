> This is a list of possible features that could be added to the library.


# LogicFormula class
List of functionalities related to the implementation of the `LogicFormula` class.

## Formula parsing

* [ ] **From string**: parse string and generate an LogicFormula object tree
```python
LogicFormula.from_string(string) -> LogicFormula
```

## Formula analysis

* [X] **Get atoms**: returns a list containing all atoms of the formula.
```python
LogicFormula.get_atoms(self) -> list[LogicFormula]
```
* [X] **Get subformulas**: returns a list containing all subformulas of the current formula.
```python
LogicFormula.get_subformulas(self) -> list[LogicFormula]
```
* [X] **Evaluate**: receives truth values for every atom and reduces the formula to a boolean or LogicFormula object.
```python
LogicFormula.evaluate(self, interpretation: dict) -> Union[bool, LogicFormula]
```
* [X] **Get Truth table**: generates a truth table for the logical formula.
```python
LogicFormula.get_truth_table(self) -> pd.DataFrame
```
* [ ] **Is tautology**: decides if formula is a tautology.
```python
LogicFormula.is_tautology(self) -> bool
```
* [ ] **Is contradiction**: decides if formula is a contradiction.
```python
LogicFormula.is_contradiction(self) -> bool
```
* [ ] **Is satisfiable**: decides if formula is satisfiable.
```python
LogicFormula.is_satisfiable(self) -> bool
```
* [ ] **Is falsifiable**: decides if formula is falsifiable.
```python
LogicFormula.is_falsifiable(self) -> bool
```
* [ ] **Is equivalent**: decides if two logic formulas are logically equivalent.
```python
LogicFormula.is_equivalent(self, other: LogicFormula) -> bool
```
* [ ] **Is CNF**: decides if formula is in Conjunctive Normal Form.
```python
LogicFormula.is_cnf(self) -> bool
```
* [ ] **Is DNF**: decides if formula is in Disjunctive Normal Form.
```python
LogicFormula.is_dnf(self) -> bool
```
* [ ] **Get disjuncts**: list all disjuncts of a formula in Conjunctive Normal Form.
```python
LogicFormula.get_disjuncts(self) -> list[LogicFormula]
```
* [ ] **Get conjuncts**: list all conjuncts of a formula in Disjunctive Normal Form.
```python
LogicFormula.get_conjuncts(self) -> list[LogicFormula]
```


## Formula manipulation

* [ ] **To CNF**: converts a formula to its Conjunctive Normal Form (without simplifications).
```python
LogicFormula.to_cnf(self) -> LogicFormula
```
* [ ] **To DNF**: converts a formula to its Disjunctive Normal Form (without simplifications).
```python
LogicFormula.to_dnf(self) -> LogicFormula
```
* [ ] **Simplify**: simplifies formula by applying logical equivalences.
```python
LogicFormula.simplify(self) -> LogicFormula
```
* [ ] **Substitute**: substitutes one proposition for another in the logic formula.
```python
LogicFormula.substitute(self, substitutions: dict)
```

## Formula visualization

* [X] **Set symbols**: sets the formula representation, with symbols provided by a dictionary.
```python
LogicFormula.set_symbols(cls, symbols: dict[str])
```
* [X] **To LaTeX**: returns a LaTeX string representation of the logic formula.
```python
LogicFormula.to_latex(self) -> str
```
* [X] **To LaTeX TikZ**: returns a LaTeX string representation of the logic formula's parse tree for the TikZ package.
```python
LogicFormula.to_latex_tikz(self, tikz_parameters, use_spaces) -> str
```
* [ ] **To LaTeX forest**: returns a LaTeX string representation of the logic formula's parse tree for the 'forest' package.
```python
LogicFormula.to_latex_forest(self, fores_parameters, use_spaces) -> str
```


# Proofs
List of possible proof-related functions.

* [ ] **Prove by Proof Tree**: finds a proof through a proof tree.
```python
proof_tree(antecedent: list[LogicFormula], succedent: LogicFormula)
```
* [ ] **Prove by Natural Deduction**: finds a proof using natural deduction.
```python
natural_deduction(antecedent: list[LogicFormula], succedent: LogicFormula)
```


<!-- Item template

* [ ] **Name**: description
```python
function(*parameters)
```

-->