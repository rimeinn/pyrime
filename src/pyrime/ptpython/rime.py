r"""Rime for Ptpython
=====================

"""

from dataclasses import dataclass

from ptpython.python_input import PythonInput

from .ime import IME
from .layout import RimeLayout


@dataclass
class _PythonInput:
    r"""An empty class to make repl as first argument of ``__init__()``"""

    repl: PythonInput


@dataclass
class Rime(IME, _PythonInput):
    r"""Rime for ptpython."""

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.layout = RimeLayout(self.repl.app, self.repl.get_input_prompt)
        super().__post_init__()
