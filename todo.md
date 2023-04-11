> This is a list of possible features that could be added to the library.


# LogicFormula class
List of functionalities related to the implementation of the `LogicFormula` class.

## Formula parsing

* [ ] **From string** : _Parse string and generate an LogicFormula object tree_
```python
LogicFormula.from_string(string)
```

## Formula analysis

* [X] **Get atoms** : _returns a list containing all atoms of the formula._
```python
LogicFormula.get_atoms(self) -> list[LogicFormula]
```
* [X] **Get subformulas** : _returns a list containing all subformulas of the current formula._
```python
LogicFormula.get_subformulas(self) -> list[LogicFormula]
```
* [ ] **Evaluate** : _receives truth values for every atom and reduces the formula to a boolean or LogicFormula object._
```python
LogicFormula.evaluate(self, interpretation: dict) -> Union[bool, LogicFormula]
```
* [ ] **Truth table** : _generates the truth table of the logical formula._
```python
LogicFormula.truth_table(self) -> pd.DataFrame
```
* [ ] **Is tautology** : _decides if formula is a tautology._
```python
LogicFormula.is_tautology(self) -> bool
```
* [ ] **Is contradiction** : _decides if formula is a contradiction._
```python
LogicFormula.is_contradiction(self) -> bool
```
* [ ] **Is satisfiable** : _decides if formula is satisfiable._
```python
LogicFormula.is_satisfiable(self) -> bool
```
* [ ] **Is falsifiable** : _decides if formula is falsifiable._
```python
LogicFormula.is_falsifiable(self) -> bool
```
* [ ] **Is equivalent** : _decides if two logic formulas are logically equivalent._
```python
LogicFormula.is_equivalent(self, other: LogicFormula) -> bool
```
* [ ] **Is CNF** : _decides if formula is in Conjunctive Normal Form._
```python
LogicFormula.is_cnf(self) -> bool
```
* [ ] **Is DNF** : _decides if formula is in Disjunctive Normal Form._
```python
LogicFormula.is_dnf(self) -> bool
```
* [ ] **Get disjuncts** : _list all disjuncts of a formula in Conjunctive Normal Form._
```python
LogicFormula.get_disjuncts(self) -> list[LogicFormula]
```
* [ ] **Get conjuncts** : _list all conjuncts of a formula in Disjunctive Normal Form._
```python
LogicFormula.get_conjuncts(self) -> list[LogicFormula]
```


## Formula manipulation

* [ ] **To CNF** : _converts a formula to its Conjunctive Normal Form (without simplifications)._
```python
LogicFormula.to_cnf(self) -> LogicFormula
```
* [ ] **To DNF** : _converts a formula to its Disjunctive Normal Form (without simplifications)._
```python
LogicFormula.to_dnf(self) -> LogicFormula
```
* [ ] **Simplify** : _simplifies formula by applying logical equivalences._
```python
LogicFormula.simplify(self) -> LogicFormula
```
* [ ] **Substitute** : _substitutes one proposition for another in the logic formula._
```python
LogicFormula.substitute(self, substitutions: dict)
```

## Formula visualization

* [X] **Set symbols** : _sets the formula representation, with symbols provided by a dictionary._
```python
LogicFormula.set_symbols(cls, symbols: dict[str])
```
* [X] **To LaTeX** : _returns a LaTeX string representation of the logic formula._
```python
LogicFormula.to_latex(self) -> str
```
* [X] **To LaTeX TikZ** : _returns a LaTeX string representation of the logic formula's parse tree for the TikZ package._
```python
LogicFormula.to_latex_tikz(self, tikz_parameters, use_spaces) -> str
```
* [ ] **To LaTeX forest** : _returns a LaTeX string representation of the logic formula's parse tree for the 'forest' package._
```python
LogicFormula.to_latex_forest(self, fores_parameters, use_spaces) -> str
```


# Proofs
List of possible proof-related functions.

* [ ] **Prove by Proof Tree** : _finds a proof through a proof tree._
```python
proof_tree(antecedent: list[LogicFormula], succedent: LogicFormula)
```
* [ ] **Prove by Natural Deduction** : _finds a proof using natural deduction._
```python
natural_deduction(antecedent: list[LogicFormula], succedent: LogicFormula)
```


<!-- Item template

* [ ] **Name** : _description_
```python
function(*parameters)
```

-->