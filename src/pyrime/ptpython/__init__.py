r"""Prompt Toolkit
==================

gdb's python cannot source binary python module.

When ``pyrime.prompt_toolkit.rime`` cannot be imported, ``RimeBase`` will
provide a support for ``pyrime.prompt_toolkit.plugins``.
"""

from dataclasses import dataclass

from prompt_toolkit.filters import Condition
from ptpython.repl import PythonRepl


@dataclass
class RimeBase:
    r"""RimeBase."""

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

    def filter(self, condition: Condition | None = None) -> Condition:
        r"""Filter.

        :param condition:
        :type condition: Condition | None
        :rtype: Condition
        """

        @Condition
        def _(condition: Condition | None = condition) -> bool:
            r""".

            :param condition:
            :type condition: Condition | None
            :rtype: bool
            """
            if condition is None:
                return self.preedit == ""
            return self.preedit == "" and condition()

        return _

    def mode(self, keys: list[str]) -> Condition:
        r"""Mode.

        :param keys:
        :type keys: list[str]
        :rtype: Condition
        """

        @Condition
        def _(keys: list[str] = keys) -> bool:
            r""".

            :param keys:
            :type keys: list[str]
            :rtype: bool
            """
            if len(keys) == 1 == len(keys[0]):
                return self.is_enabled
            elif len(keys) == 1 or len(keys) > 1 and keys[0] == "escape":
                return self.preedit != ""
            else:
                raise NotImplementedError

        return _
