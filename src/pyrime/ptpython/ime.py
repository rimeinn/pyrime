r"""IME
=======

``ptpython`` use a multi mode editor with emacs, vi insert, vi normal modes,
... So we must know current edit mode to decide how to handle key inputs.
``IME`` provide a skeleton for it.
"""

from dataclasses import dataclass

from prompt_toolkit.filters import Condition
from prompt_toolkit.filters.app import emacs_insert_mode, vi_insert_mode
from prompt_toolkit.filters.base import Filter
from ptpython.repl import PythonRepl

from ..ime import IMEBase


@dataclass
class IME(IMEBase):
    r"""IME is a class to provide basic supports for ``ptpython`` 's plugins:
    ``repl``, ``filter()``, ``is_enabled``.
    """

    repl: PythonRepl
    iminsert: bool = False

    @property
    def has_preedit(self) -> bool:
        return False

    @property
    def preedit_available(self) -> Condition:
        r"""Filter. Only when ``preedit`` is not available, key binding works.

        :rtype: Condition
        """

        @Condition
        def _() -> bool:
            r""".

            :rtype: bool
            """
            return self.has_preedit

        return _

    @property
    def insert_mode(self) -> Filter:
        r"""Filter. Only when ``preedit`` is not available, key binding works.

        :rtype: Filter
        """

        return (emacs_insert_mode | vi_insert_mode) & ~self.preedit_available
