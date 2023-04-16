from __future__ import annotations
import warnings


class LogicFormula:
    """
    Represents a logic formula of propositional logic.

    A logic formula is a tree-like structure composed of logical operators and atomic propositions.
    The class stores the formula's operators and components, where components are either atomic
    propositions or other logic formulas.

    Attributes
    ----------
    _operator: str
        The operator of the logic formula, one of {atom, ~, &, |, ->, <->}

    _components: str or LogicFormula objects
        The components of the logic formula, that are strings or LogicFormula objects.

    Notes
    -----
    The class supports the use of Python's binary operators to construct formulas, with the following
    mapping between binary and logical operators:

    - ~ represents negation ('not')
    - & represents conjunction ('and')
    - | represents disjunction ('or')
    - >> represents implication ('if.. then')
    - << represents equality ('if and only if')

    Warning: The shift operators (>> and <<) have precedence over the operators & and |.
    Use parentheses to enforce the correct order of operations when using this style.

    Examples
    --------
    >>> P = LogicFormula.atom('P')
    >>> Q = LogicFormula.atom('Q')
    >>> P.negation().conjunction(Q.implication(P))
    LogicFormula(¬P ∧ (Q → P))
    >>> ~(P & Q) << (~P | ~Q)
    LogicFormula(¬(P ∧ Q) ↔ ¬P ∨ ¬Q)

    """

    _valid_operators = ("atom", "~", "&", "|", "->", "<->")
    _unicode_dict = {"~": "¬", "&": "∧", "|": "∨", "->": "→", "<->": "↔"}
    _utf_dict = {
        "~": "\u00AC",
        "&": "\u2227",
        "|": "\u2228",
        "->": "\u2192",
        "<->": "\u2194",
    }
    _latex_dict = {
        "~": r"\lnot ",
        "&": r"\land",
        "|": r"\lor",
        "->": r"\rightarrow",
        "<->": r"\leftrightarrow",
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

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return other == str(self)
        if self.operator() == other.operator():
            if self.operator() in ("atom", "~"):
                return self.components() == other.components()
            return all(
                self_subf == other_subf
                for self_subf, other_subf in zip(self.components(), other.components())
            )

    def __iter__(self) -> LogicFormula:
        return iter(self.get_subformulas())

    def __hash__(self) -> int:
        return hash(str(self))

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

    @staticmethod
    def random(n: int, atom_list=None) -> LogicFormula:
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
            return LogicFormula.random(n - 1, atom_list).negation()
        return LogicFormula(
            operator,
            LogicFormula.random(n // 2, atom_list),
            LogicFormula.random(n - n // 2, atom_list),
        )

    def is_atomic(self) -> bool:
        """Determines if the current formula is an atom or not."""
        return self.operator() == "atom"

    def get_atoms(self) -> list[LogicFormula]:
        """
        Returns a list containing all atoms of the formula.

        Returns
        -------
        atoms: list of str
            A list of all atoms of the current formula.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q, R
        >>> ((R >> (P & Q)) | P).get_atoms()
        [LogicFormula(P), LogicFormula(Q), LogicFormula(R)]

        """
        if self.is_atomic():
            return [self]
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

        Returns
        -------
        subformulas: list of str
            A list of all subformulas of the current formula.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q
        >>> (P >> (P & ~Q)).get_subformulas()
        [LogicFormula(P),
        LogicFormula(Q),
        LogicFormula(¬Q),
        LogicFormula(P ∧ ¬Q),
        LogicFormula(P → P ∧ ¬Q)]

        """
        if self.is_atomic():
            return [self]
        else:
            subformulas = [self]
            for subformula in self.components():
                subformulas.extend(subformula.get_subformulas())
        return sorted(set(subformulas), key=lambda f: (len(str(f)), str(f)))

    def evaluate(self, valuation: dict[bool]) -> bool:
        """
        Evaluates the formula using the truth values given by a dictionary.

        Parameters
        ----------
        valuation: dict of bool
            A dictionary mapping atomic propositions to boolean truth values.
            The keys can be either atomic LogicFormula objects or the atoms string representations.

        Returns
        -------
        truth_value: bool
            The truth value of the logic formula.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q
        >>> (P >> (P & ~Q)).evaluate({P: True, Q: False})
        True
        >>> (P & Q).evaluate({"P": True, "Q": False})
        False

        """
        if self.is_atomic():
            return (
                valuation[self]
                if self in valuation.keys()
                else valuation[self.components()[0]]
            )
        elif self.operator() == "~":
            return not self.components()[0].evaluate(valuation)
        left, right = self.components()
        if self.operator() == "&":
            return left.evaluate(valuation) and right.evaluate(valuation)
        elif self.operator() == "|":
            return left.evaluate(valuation) or right.evaluate(valuation)
        elif self.operator() == "->":
            return (not left.evaluate(valuation)) or right.evaluate(valuation)
        elif self.operator() == "<->":
            return left.evaluate(valuation) == right.evaluate(valuation)

    def get_truth_table(self, show_intermediate=True, to_list=False):
        """
        Generates the truth table of the logical formula.

        Notes
        -----
        By default, the table is returned as a pandas.DataFrame object. If the Pandas package is
        not found, the method returns a list of lists instead.

        Parameters
        ----------
        show_intermediate: bool, optional
            Decides if the truth table should contain the intermediate results.
            Default value is True.

        to_list: bool, optional
            Decides if the return value should be a list of lists instead of a DataFrame object.
            Default value is False.

        Returns
        -------
        truth_table: pandas.DataFrame or list of lists
            The truth table of the logical formula.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q, DE_MORGAN_AND
        >>> (P >> ~Q).get_truth_table(to_list=True)
        [[LogicFormula(P), LogicFormula(Q), LogicFormula(¬Q), LogicFormula(P → ¬Q)],
         [True, True, False, False],
         [True, False, True, True],
         [False, True, False, True],
         [False, False, True, True]]

        """
        from itertools import product

        if not to_list:
            try:
                from pandas import DataFrame
            except ImportError:
                warnings.warn(
                    "Optional dependency 'pandas' not found. Falling back to a list of lists.",
                    ImportWarning,
                )
                DataFrame = None

        atoms = self.get_atoms()
        if show_intermediate:
            subformulas = self.get_subformulas()
        else:
            subformulas = atoms + [self]
        table = []
        valuation_dicts = [
            {atom: value for atom, value in zip(atoms, valuation)}
            for valuation in product((True, False), repeat=len(atoms))
        ]
        for valuation in valuation_dicts:
            table.append([formula.evaluate(valuation) for formula in subformulas])
        return (
            [subformulas] + table
            if to_list or DataFrame is None
            else (DataFrame(table, columns=subformulas))
        )

    def is_tautology(self) -> bool:
        """Checks if the logical formula is a tautology, i.e., it evaluates to true
        for all possible valuations."""
        truth_table = self.get_truth_table(show_intermediate=True, to_list=True)[1:]
        return all(row[-1] for row in truth_table)

    def is_contradiction(self) -> bool:
        """Checks if the logical formula is a contradiction, i.e., it evaluates to false
        for all possible valuations."""
        truth_table = self.get_truth_table(show_intermediate=True, to_list=True)[1:]
        return all(not row[-1] for row in truth_table)

    def is_satisfiable(self) -> bool:
        """Checks if the logical formula is satisfiable, i.e., it evaluates to true
        for at least one valuation."""
        return not self.is_contradiction()

    def get_satisfiable_valuations(self, string_atoms=False) -> list[dict]:
        r"""
        Returns a list of valuations that satisfy the logical formula.

        Parameters
        ----------
        string_atoms: bool, optional
            Decides if the keys in the valuation dictionaries should be string representations of
            the atoms, instead of the LogicFormula objects.
            Default value is False.

        Returns
        -------
        satisfiable_valuations: list of dict
            List of all valuations that satisfy the logical formula.
            Each element of the list is a dictionary, with atoms as keys and their corresponding
            boolean values.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q
        >>> implication = P >> Q
        >>> print(implication.get_satisfiable_valuations())
        [{LogicFormula(P): True, LogicFormula(Q): True},
         {LogicFormula(P): False, LogicFormula(Q): True},
         {LogicFormula(P): False, LogicFormula(Q): False}]
        >>> implication.get_satisfiable_valuations(string_atoms=True)
        [{'P': True, 'Q': True},
         {'P': False, 'Q': True},
         {'P': False, 'Q': False}]

        """
        truth_table = self.get_truth_table(show_intermediate=False, to_list=True)
        atoms = truth_table[0][:-1]
        return [
            {
                str(atom) if string_atoms else atom: value
                for atom, value in zip(atoms, row)
            }
            for row in truth_table[1:]
            if row[-1]
        ]

    def is_falsifiable(self) -> bool:
        """Checks if the logical formula is falsifiable, i.e., it evaluates to false
        for at least one valuation."""
        return not self.is_tautology()

    def get_falsifiable_valuations(self, string_atoms=False) -> list[dict]:
        """
        Returns a list of valuations that falsify the logical formula.

        Parameters
        ----------
        string_atoms: bool, optional
            Decides if the keys in the valuation dictionaries should be string representations of
            the atoms, instead of the LogicFormula objects.
            Default value is False.

        Returns
        -------
        falsifiable_valuations: list of dict
            List of all valuations that falsify the logical formula.
            Each element of the list is a dictionary, with atoms as keys and their corresponding
            boolean values.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q
        >>> implication = P >> Q
        >>> implication.get_falsifiable_valuations()
        [{LogicFormula(P): True, LogicFormula(Q): False}]
        >>> implication.get_falsifiable_valuations(string_atoms=True)
        [{'P': True, 'Q': False}]

        """
        truth_table = self.get_truth_table(show_intermediate=False, to_list=True)
        atoms = truth_table[0][:-1]
        return [
            {
                str(atom) if string_atoms else atom: value
                for atom, value in zip(atoms, row)
            }
            for row in truth_table[1:]
            if not row[-1]
        ]

    def is_equivalent(self, other: LogicFormula) -> bool:
        """
        Checks if the current formula is logically equivalent to another formula instance.

        Parameters
        ----------
        other: LogicFormula
            The other LogicFormula object to be compared with the current formula.

        Examples
        --------
        >>> from pyproplogic.commonformulas import P, Q
        >>> P.is_equivalent(Q)
        False
        >>> P.is_equivalent(P | Q)
        False
        >>> (P & Q).is_equivalent(Q & P)
        True
        >>> (~(P & ~P)).is_equivalent(Q | ~Q)
        True

        """
        return self.biconditional(other).is_tautology()

    @classmethod
    def get_symbols(cls) -> dict[str]:
        """Returns the symbol dictionary with the logical operators and its current representation"""
        return cls._current_dict

    @classmethod
    def set_symbols(cls, symbols: dict[str]):
        """
        Sets the formula representation, with symbols provided by a dictionary.

        Parameters
        ----------
        symbols: dict of str
            A dictionary containing the symbols to use.
            The dictionary doesn't need to be complete; any missing symbol will stay unchanged.

        Examples
        --------
        >>> P = LogicFormula.atom("P")
        >>> Q = LogicFormula.atom("Q")
        >>> formula = P >> ~(P & Q)
        >>> print(formula)
        P → ¬(P ∧ Q)
        >>> LogicFormula.set_symbols({"&": "AND", "->": "IMPLIES"})
        >>> print(formula)
        P IMPLIES ¬(P AND Q)

        See Also:
        ---------
        - `LogicFormula.set_unicode_symbols()` sets the representation to Unicode.
        - `LogicFormula.set_utf_symbols()` sets the representation to UTF-8.
        - `LogicFormula.set_ascii_symbols()` sets the representation to ASCII.
        - `LogicFormula.set_latex_symbols()` sets the representation to LaTeX.

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
        r"""
        Returns a LaTeX string representation of the logic formula, with operators replaced by
        LaTeX commands.

        Returns
        -------
        latex_formula: str
            A string of LaTeX code that produces the symbolic representation of the logic formula.

        Examples
        --------
        >>> P = LogicFormula.atom('P')
        >>> Q = LogicFormula.atom('Q')
        >>> formula = ~(P & (Q >> P))
        >>> print(formula.to_latex())
        \lnot (P \land (Q \rightarrow P))

        """
        previous_dict = LogicFormula._current_dict
        LogicFormula.set_latex_symbols()
        latex_formula = str(self)
        LogicFormula._current_dict = previous_dict
        return latex_formula

    def to_latex_tikz(
        self, tikz_parameters="sibling distance=25mm/#1", use_tabs=False
    ) -> str:
        r"""
        Returns a LaTeX string representation of the logic formula's parse tree for the TikZ package.

        Parameters
        ----------
        tikz_parameters: str, optional
            String of TikZ parameters that will be used to customize the parse tree.
            Default value is 'sibling distance=25mm/#1'.

        use_tabs: bool, optional
            Boolean that indicates if tabs should be used instead of spaces.
            Default value is False.

        Returns
        -------
        tikz_code: str
            A string of LaTeX code that produces the a graphical representation of the parse tree of
            the logic formula using the TikZ package.

        Examples
        --------
            >>> P = LogicFormula.atom('P')
            >>> Q = LogicFormula.atom('Q')
            >>> formula = P >> Q
            >>> print(formula.to_latex_tikz())
            \begin{tikzpicture}
            [level/.style={sibling distance=25mm/#1}]
                \node {$\rightarrow$}
                    child {node {$P$}}
                    child {node {$Q$}};
            \end{tikzpicture}

        """
        latex = LogicFormula._latex_dict
        tab = "\t" if use_tabs else " " * 4
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
