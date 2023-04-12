from __future__ import annotations


class LogicFormula:
    """
    Represents a logic formula of propositional logic.

    A logic formula is a tree-like structure composed of logical operators and atomic propositions.
    The class stores the formula's operators and components, where components are either atomic
    propositions or other logic formulas.

    Attributes:
    -----------
    _operator : str
        The operator of the logic formula, one of {atom, ~, &, |, ->, <->}

    _components : str or LogicFormula objects
        The components of the logic formula, that are strings or LogicFormula objects.

    Notes:
    ------
    The class supports the use of Python's binary operators to construct formulas, with the following
    mapping between binary and logical operators:

    - ~ represents negation ('not')
    - & represents conjunction ('and')
    - | represents disjunction ('or')
    - >> represents implication ('if.. then')
    - << represents equality ('if and only if')

    Warning: The shift operators (>> and <<) have precedence over the operators & and |.
    Use parentheses to enforce the correct order of operations when using this style.

    Examples:
    ---------
    >>> p = LogicFormula.atom('p')
    >>> q = LogicFormula.atom('q')
    >>> p.negation().conjunction(q.implication(p))
    LogicFormula(¬p ∧ (q → p))
    >>> print(~(p & q) << (~p | ~q))
    ¬(p ∧ q) ↔ ¬p ∨ ¬q

    """

    _valid_operators = {"atom", "~", "&", "|", "->", "<->"}
    _unicode_dict = {"~": "¬", "&": "∧", "|": "∨", "->": "→", "<->": "↔"}
    _utf_dict = {
        "~": "\u00AC",
        "&": "\u2227",
        "|": "\u2228",
        "->": "\u2192",
        "<->": "\u2194",
    }
    _latex_dict = {
        "~": "\\lnot ",
        "&": "\\land",
        "|": "\\lor",
        "->": "\\rightarrow",
        "<->": "\\leftrightarrow",
    }
    _current_dict = _unicode_dict

    def __init__(self, operator: str, *components: LogicFormula):
        if operator not in LogicFormula._valid_operators:
            raise ValueError("invalid operator: " + operator)
        if operator in ["atom", "~"] and len(components) != 1:
            raise ValueError(
                f"unary operator '{operator}' requires exactly 1 component"
            )
        if operator not in ["atom", "~"] and len(components) != 2:
            raise ValueError(
                f"binary operator '{operator}' requires exactly 2 components"
            )
        self._operator = operator
        self._components = components

    def __str__(self) -> str:
        if self.operator() == "atom":
            return self.components()[0]
        precedence = {"atom": 4, "~": 3, "&": 2, "|": 2, "->": 1, "<->": 1}
        subformula_str = [
            f"({subformula})"
            if precedence[subformula.operator()] <= precedence[self.operator()]
            else str(subformula)
            for subformula in self.components()
        ]
        if self.operator() == "~":
            return LogicFormula._current_dict["~"] + subformula_str[0]
        elif self.operator() in LogicFormula._current_dict:
            return f" {LogicFormula._current_dict[self.operator()]} ".join(
                subformula_str
            )

    def __repr__(self) -> str:
        return f"LogicFormula({self.__str__()})"

    def __contains__(self, item: LogicFormula) -> bool:
        if not isinstance(item, LogicFormula):
            raise TypeError(
                f"'in' requires LogicFormula as left operand, not {type(item).__name__}"
            )
        return (item.to_ascii()) in (self.to_ascii())

    def __iter__(self) -> LogicFormula:
        return iter(self.get_subformulas())

    def operator(self) -> str:
        """Returns the logic operator of the current formula."""
        return self._operator

    def components(self) -> tuple[LogicFormula]:
        """Returns a tuple containing the component(s) of the current formula."""
        return self._components

    @staticmethod
    def atom(symbol: str) -> LogicFormula:
        """Creates a LogicFormula object containing an atom with the given symbol."""
        return LogicFormula("atom", symbol)

    def negation(self) -> LogicFormula:
        """Creates a LogicFormula object containing the negation of self."""
        return LogicFormula("~", self)

    def __invert__(self):
        return LogicFormula("~", self)

    def conjunction(self, other) -> LogicFormula:
        """Creates a LogicFormula object containing a conjunction between self and other."""
        return LogicFormula("&", self, other)

    def __and__(self, other) -> LogicFormula:
        return LogicFormula("&", self, other)

    def disjunction(self, other) -> LogicFormula:
        """Creates a LogicFormula object containing a disjunction between self and other."""
        return LogicFormula("|", self, other)

    def __or__(self, other) -> LogicFormula:
        return LogicFormula("|", self, other)

    def implication(self, other) -> LogicFormula:
        """Creates a LogicFormula object containing an implication from self to other."""
        return LogicFormula("->", self, other)

    def __rshift__(self, other) -> LogicFormula:
        return LogicFormula("->", self, other)

    def biconditional(self, other) -> LogicFormula:
        """Creates a LogicFormula object containing a biconditional between self and other."""
        return LogicFormula("<->", self, other)

    def __lshift__(self, other) -> LogicFormula:
        return LogicFormula("<->", self, other)

    def is_atomic(self) -> bool:
        """Determines if the current formula is an atom or not."""
        return self.operator() == "atom"

    def get_atoms(self) -> list[LogicFormula]:
        """
        Returns a list containing all atoms of the formula.

        Returns:
        --------
        atoms : list of str
            A list of all atoms of the current formula.

        """
        if self.is_atomic():
            return self
        atoms = []
        for subformula in self.components():
            atoms.extend(subformula.get_atoms())
        return sorted(set(atoms), key=str)

    def get_subformulas(self) -> list[LogicFormula]:
        """
        Returns a list containing all subformulas of the current formula.

        * If the current formula is an atomic formula, returns itself
        * If the current formula is a complex formula, creates a list with it and recursively
        calls this method on its subformulas, appending the results to the list, which is then
        sorted and returned with duplicates removed.

        Returns:
        --------
        subformulas : list of str
            A list of all subformulas of the current formula.

        """
        if self.is_atomic():
            return [self]
        else:
            subformulas = [self]
            for subformula in self.components():
                subformulas.extend(subformula.get_subformulas())
        return sorted(set(subformulas), key=str)

    def evaluate(self, truth_values: dict[bool]) -> bool:
        """
        Evaluates the formula using the truth values given by a dictionary.

        Parameters:
        -----------
        truth_values: dict of bool
            A dictionary mapping atomic propositions to boolean truth values.

        Returns:
        bool
            The truth value of the logic formula.

        """
        if self.is_atomic():
            return (
                truth_values[self]
                if self in truth_values
                else truth_values[self.components()[0]]
            )
        elif self.operator() == "~":
            return not self.components()[0].evaluate(truth_values)
        left, right = self.components()
        if self.operator() == "&":
            return left.evaluate(truth_values) and right.evaluate(truth_values)
        elif self.operator() == "|":
            return left.evaluate(truth_values) or right.evaluate(truth_values)
        elif self.operator() == "->":
            return (not left.evaluate(truth_values)) or right.evaluate(truth_values)
        elif self.operator() == "<->":
            return left.evaluate(truth_values) == right.evaluate(truth_values)

    @classmethod
    def get_symbols(cls) -> dict[str]:
        """Returns the symbol dictionary with the logical operators and its current representation"""
        return cls._current_dict

    @classmethod
    def set_symbols(cls, symbols: dict[str]):
        """
        Sets the formula representation, with symbols provided by a dictionary.

        Parameters:
        -----------
        symbols: dict of str
            A dictionary containing the symbols to use.
            The dictionary doesn't need to be complete; any missing symbol will stay unchanged.

        """
        cls._current_dict = {
            key: symbols.get(key, cls.get_symbols()[key])
            for key in cls.get_symbols().keys()
        }

    @classmethod
    def set_unicode_symbols(cls):
        """Sets the symbol dictionary to use Unicode symbols for the logical operators."""
        cls._current_dict = cls._unicode_dict

    def to_unicode(self) -> str:
        """Returns the formula as an Unicode string."""
        previous_dict = LogicFormula._current_dict
        LogicFormula.set_unicode_symbols()
        unicode_formula = str(self)
        LogicFormula._current_dict = previous_dict
        return unicode_formula

    @classmethod
    def set_utf_symbols(cls):
        """Sets the symbol dictionary to use UTF-8 symbols for the logical operators."""
        cls._current_dict = cls._utf_dict

    def to_utf(self) -> str:
        """Returns the formula as an UTF-8 string."""
        previous_dict = LogicFormula._current_dict
        LogicFormula.set_utf_symbols()
        utf_formula = str(self)
        LogicFormula._current_dict = previous_dict
        return utf_formula

    @classmethod
    def set_ascii_symbols(cls):
        """Sets the symbol dictionary to use ASCII symbols for the logical operatos."""
        cls._current_dict = {key: key for key in cls._current_dict.keys()}

    def to_ascii(self) -> str:
        """Returns the formula as an ASCII string."""
        previous_dict = LogicFormula._current_dict
        LogicFormula.set_ascii_symbols()
        ascii_formula = str(self)
        LogicFormula._current_dict = previous_dict
        return ascii_formula

    @classmethod
    def set_latex_symbols(cls):
        """Sets the symbol dictionary to use LaTeX commands for the logical operators."""
        cls._current_dict = cls._latex_dict

    def to_latex(self) -> str:
        """
        Returns a LaTeX string representation of the logic formula, with operators replaced by
        LaTeX commands.

        Returns:
        --------
        latex_formula : str
            A string of LaTeX code that produces the symbolic representation of the logic formula.

        Examples:
        ---------
        >>> p = LogicFormula.atom('p')
        >>> q = LogicFormula.atom('q')
        >>> formula = (p.conjunction(q.implication(p))).negation()
        >>> print(formula.to_latex())
        \lnot (p \land (q \\rightarrow p))

        """
        previous_dict = LogicFormula._current_dict
        LogicFormula.set_latex_symbols()
        latex_formula = str(self)
        LogicFormula._current_dict = previous_dict
        return latex_formula

    def to_latex_tikz(
        self, tikz_parameters="sibling distance=25mm/#1", use_spaces=False
    ) -> str:
        """
        Returns a LaTeX string representation of the logic formula's parse tree for the TikZ package.

        Parameters:
        -----------
        tikz_parameters : str, optional
            String of TikZ parameters that will be used to customize the parse tree.
            Default value is 'sibling distance=25mm/#1'.

        use_spaces : bool, optional
            Boolean that indicates if spaces should be used instead of tabs.
            Default value is False.

        Returns:
        --------
        tikz_code : str
            A string of LaTeX code that produces the a graphical representation of the parse tree of
            the logic formula using the TikZ package.

        Examples:
        ---------
            >>> p = LogicFormula.atom('p')
            >>> q = LogicFormula.atom('q')
            >>> formula = p.implication(q)
            >>> print(formula.to_latex_tikz())
            \\begin{tikzpicture}
            [level/.style={sibling distance=25mm/#1}]
                \\node {$\\rightarrow$}
                    child {node {$p$}}
                    child {node {$q$}};
            \end{tikzpicture}

        """
        latex = LogicFormula._latex_dict
        tab = " " * 4 if use_spaces else "\t"
        child_template = "child {{node {{${}$}}"

        def parse_tree(formula: LogicFormula, level=1) -> str:
            identation = tab * level
            if formula.is_atomic():
                return identation + child_template.format(str(formula)) + "}"
            string = identation + child_template.format(latex[formula.operator()])
            for subformula in formula.components():
                string += "\n" + identation + parse_tree(subformula, level + 1)
            string += "}"
            return string

        if self.is_atomic():
            return f"{tab}\\node {{${self.operator()}$}}"
        string = f"{tab}\\node {{${latex[self.operator()]}$}}"
        for subformula in self.components():
            string += "\n" + tab + parse_tree(subformula)
        string += ";"
        tikz_code = (
            "\\begin{{tikzpicture}}\n"
            "[level/.style={{{}}}]\n"
            "{}\n"
            "\\end{{tikzpicture}}"
        )
        return tikz_code.format(tikz_parameters, string)
