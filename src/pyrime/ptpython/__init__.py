r"""Ptpython
============

``ptpython`` use a multi mode editor with emacs, vi insert, vi normal modes,
... So we must know current edit mode to decide how to handle key inputs.
``IME`` provide a skeleton for it.
"""

from dataclasses import dataclass

from prompt_toolkit.filters import Condition
from ptpython.repl import PythonRepl


@dataclass
class IME:
    r"""IME is a class to provide basic support for ``ptpython``."""

    repl: PythonRepl
    preedit: str = ""
    is_enabled: bool = False

    def conditional_disable(self) -> None:
        r"""Conditional disable.

        :rtype: None
        """

    def conditional_enable(self) -> None:
        r"""Conditional enable.

        :rtype: None
        """

    def filter(self) -> Condition:
        r"""Filter. Only when ``preedit`` is empty, key binding works.

        :rtype: Condition
        """

        @Condition
        def _() -> bool:
            r""".

            :rtype: bool
            """
            return self.preedit == ""

        return _
