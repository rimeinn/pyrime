r"""Rime for Ptpython
=====================

"""

from dataclasses import dataclass, field

from ptpython.python_input import PythonInput

from .ime import IME
from .layout import RimeLayout


@dataclass
class _Rime:
    r"""An empty class to make repl as first argument of ``__init__()``"""

    repl: PythonInput


@dataclass
class Rime(IME, _Rime):
    r"""Rime for ptpython."""

    layout: RimeLayout = field(init=False, default_factory=RimeLayout)

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.layout = RimeLayout(self.repl.app, self.repl.get_input_prompt)
        super().__post_init__()
