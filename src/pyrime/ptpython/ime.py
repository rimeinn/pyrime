r"""IME
=======

``ptpython`` use a multi mode editor with emacs, vi insert, vi normal modes,
... So we must know current edit mode to decide how to handle key inputs.
``IME`` provide a skeleton for it.
"""

from dataclasses import dataclass

from prompt_toolkit.filters import Condition
from ptpython.repl import PythonRepl

from ..ime import IMEBase


@dataclass
class IME(IMEBase):
    r"""IME is a class to provide basic supports for ``ptpython`` 's plugins:
    ``repl``, ``filter()``, ``enable()``, ``disable()``, ``toggle()``.
    """

    repl: PythonRepl

    def __post_init__(self):
        super().__post_init__()

    @property
    def has_preedit(self) -> bool:
        return False

    def filter(self) -> Condition:
        r"""Filter. Only when ``preedit`` is empty, key binding works.

        :rtype: Condition
        """

        @Condition
        def _() -> bool:
            r""".

            :rtype: bool
            """
            return not self.has_preedit

        return _
