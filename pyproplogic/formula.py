from __future__ import annotations
from typing import Union

class LogicFormula:
    """
    Represents a logic formula of propositional logic.

    A logic formula is a tree-like structure composed of logical operators and atomic propositions.
    The class stores the formula's operators and components, where components are either atomic
    propositions or other logic formulas.

    Attributes:
    -----------
    _operator : str
        The operator of the logic formula, one of {'atom', '~', '&', '|', '->', '<->'}
    _components : str or LogicFormula objects
        The components of the logic formula, that are strings or LogicFormula objects.

    Notes:
    ------
    The binary operators '&' and '|' can also be used in place of the methods LogicFormula.conjunction
    and LogicFormula.disjunction.
        
    Examples:
    ---------
    >>> p = LogicFormula.atom('p')
    >>> q = LogicFormula.atom('q')
    >>> p.conjunction(q)
    LogicFormula(p ∧ q)
    >>> (p & q).implication(p.implication(q.negation()))
    LogicFormula(p ∧ q → (¬q → p))

    """
    _symbol_dict = {'~': '¬', '&': '∧', '|': '∨', '->': '→', '<->': '↔'}
    
    def __init__(self, operator: str, *components: LogicFormula):
        if operator not in LogicFormula._valid_operators():
            raise ValueError('invalid operator: ' + operator)
        if operator in ['atom', '~'] and len(components) != 1:
            raise ValueError(f"unary operator '{operator}' requires exactly 1 component")
        if operator not in ['atom', '~'] and len(components) != 2:
            raise ValueError(f"binary operator '{operator}' requires exactly 2 components")
        self._operator = operator
        self._components = components

    def __str__(self) -> str:
        """ Returns a string representation of the logic formula, using UTF-8 symbols. """
        if self.operator() == 'atom':
            return self.components()[0]
        precedence = {'atom': 4, '~': 3, '&': 2, '|': 2, '->': 1, '<->': 1}
        subformula_str = [
            f'({subformula})' if precedence[subformula.operator()] <= precedence[self.operator()] else str(subformula)
            for subformula in self.components()
        ]
        if self.operator() == '~':
            return LogicFormula._symbol_dict['~'] + subformula_str[0]
        elif self.operator() in LogicFormula._symbol_dict:
            return f' {LogicFormula._symbol_dict[self.operator()]} '.join(subformula_str)
        
    def __repr__(self) -> str:
        return f'LogicFormula({self.__str__()})'
    
    def operator(self) -> str:
        """ Returns the logic operator of the current formula. """
        return self._operator
    
    def components(self) -> tuple[LogicFormula]:
        """ Returns a tuple containing the component(s) of the current formula. """
        return self._components

    @staticmethod
    def _valid_operators() -> tuple[str]:
        """ Returns a set containing the valid operators of propositional logic. """
        return {'atom', '~', '&', '|', '->', '<->'}
    
    @staticmethod
    def atom(symbol: str) -> LogicFormula:
        """ Creates a LogicFormula object containing an atom with the given symbol. """
        return LogicFormula('atom', symbol)

    def negation(self) -> LogicFormula:
        """ Creates a LogicFormula object containing the negation of self. """
        return LogicFormula('~', self)
    
    def conjunction(self, other) -> LogicFormula:
        """ Creates a LogicFormula object containing a conjunction between self and other. """
        return LogicFormula('&', self, other)
    
    def __and__(self, other) -> LogicFormula:
        return LogicFormula('&', self, other)
    
    def disjunction(self, other) -> LogicFormula:
        """ Creates a LogicFormula object containing a disjunction between self and other. """
        return LogicFormula('|', self, other)
    
    def __or__(self, other) -> LogicFormula:
        return LogicFormula('|', self, other)
    
    def implication(self, other) -> LogicFormula:
        """ Creates a LogicFormula object containing an implication from self to other. """
        return LogicFormula('->', self, other)
    
    def biconditional(self, other) -> LogicFormula:
        """ Creates a LogicFormula object containing a biconditional between self and other. """
        return LogicFormula('<->', self, other)
    
    def is_atomic(self) -> bool:
        """ Determines if the current formula is an atom or not. """
        return self.operator() == 'atom'

    def list_atoms(self) -> list[str]:
        """
        Returns a list containing all atoms of the current formula.

        Returns:
        --------
        atoms : list of str
            A list of all atoms of the current formula.

        """
        if self.is_atomic():
            return [self]
        atoms = []
        for subformula in self.components():
            atoms.extend(subformula.list_atoms())
        return sorted(set(atoms), key=str)
        
    def list_subformulas(self) -> list[LogicFormula]:
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
            return self
        else:
            subformulas = [self]
            for subformula in self.components():
                subformulas.extend(subformula.list_subformulas())
        return sorted(set(subformulas), key=str)
    
    @classmethod
    def get_symbols(cls) -> dict[str]:
        """ Returns the symbol dictionary with the logical operators and its current representation """
        return cls._symbol_dict

    @classmethod
    def set_symbols(cls, symbols: dict[str]):
        """
        Sets the symbol dictionary to use custom symbols given by a dictionary.
        
        Parameters:
        -----------
        symbols: dict of str
            A dictionary containing the symbols to use.
            The dictionary doesn't need to be complete; any missing symbol will stay unchanged.

        """
        cls._symbol_dict = {
            key: symbols.get(key, cls.get_symbols()[key])
            for key in cls.get_symbols().keys()
        }

    @classmethod
    def set_unicode_symbols(cls):
        """ Sets the symbol dictionary to use Unicode symbols for the logical operators. """
        cls._symbol_dict = {
            '~': '¬', 
            '&': '∧', 
            '|': '∨', 
            '->': '→', 
            '<->': '↔'
        }

    @classmethod
    def set_utf_symbols(cls):
        """ Sets the symbol dictionary to use UTF-8 symbols for the logical operators. """
        cls._symbol_dict = {
            '~': '\u00AC', 
            '&': '\u2227', 
            '|': '\u2228', 
            '->': '\u2192', 
            '<->': '\u2194'
        }

    @classmethod
    def set_ascii_symbols(cls):
        """ Sets the symbol dictionary to use ASCII symbols for the logical operatos. """
        cls._symbol_dict = {symbol:symbol for symbol in cls._symbol_dict.keys()}

    @classmethod
    def set_latex_symbols(cls):
        """ Sets the symbol dictionary to use LaTeX commands for the logical operators. """
        cls._symbol_dict = {
            '~': '\\lnot ', 
            '&': '\\land', 
            '|': '\\lor', 
            '->': '\\rightarrow', 
            '<->': '\\leftrightarrow'
        }

    def to_latex(self) -> str:
        """
        Returns a LaTeX string representation of the logic formula, with special characters replaced
        by LaTeX commands.

        Returns:
        --------
        latex_formula : str
            A string of LaTeX code that produces the symbolic representation of the logic formula.

        Examples:
        ---------
        >>> p = LogicFormula.atom('p')
        >>> q = LogicFormula.atom('q')
        >>> formula = (p & q.implication(p)).negation()
        >>> print(formula.to_latex())
        \lnot(p \land (q \\rightarrow p))
        
        """
        current_dict = LogicFormula._symbol_dict
        LogicFormula.set_latex_symbols()
        latex_formula = str(self)
        LogicFormula._symbol_dict = current_dict
        return latex_formula
    
    def to_latex_tikz(self, tikz_parameters='sibling distance=25mm/#1', use_spaces=False) -> str:
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
        latex_symbols = {
            '~': '\\lnot', 
            '&': '\\land', 
            '|': '\\lor', 
            '->': '\\rightarrow', 
            '<->': '\\leftrightarrow'
        }
        tab = ' '*4 if use_spaces else '\t'
        child_template = 'child {{node {{${}$}}'

        def parse_tree(formula: LogicFormula, level=1) -> str:
            identation = tab*level
            if formula.is_atomic():
                return identation + child_template.format(str(formula)) + '}'
            string = identation + child_template.format(latex_symbols[formula.operator()])
            for subformula in formula.components():
                string += '\n' + identation + parse_tree(subformula, level+1)
            string += '}'
            return string

        if self.is_atomic():
            return f'{tab}\\node {{${self.operator()}$}}'
        string = f'{tab}\\node {{${latex_symbols[self.operator()]}$}}'
        for subformula in self.components():
            string += '\n' + tab + parse_tree(subformula)
        string += ';'
        tikz_code =  (
            "\\begin{{tikzpicture}}\n"
            "[level/.style={{{}}}]\n"
            "{}\n"
            "\\end{{tikzpicture}}"
        )
        return tikz_code.format(tikz_parameters, string)