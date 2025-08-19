"""Prompt style
===============

Generate prompt style from ``sys.ps1``.

Experimental!
"""

# import sys
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import AnyFormattedText
from ptpython.prompt_style import IPythonPrompt

# from .ansi import ansi2prompt_toolkit

if TYPE_CHECKING:
    from ptpython.python_input import PythonInput


class PythonPrompt(IPythonPrompt):
    """A prompt resembling the IPython prompt."""

    def __init__(self, python_input: "PythonInput") -> None:
        """Init.

        :param python_input:
        :type python_input: "PythonInput"
        :rtype: None
        """
        super().__init__(python_input)
        # self.formats, self.styles = ansi2prompt_toolkit(str(sys.ps1))

    def in_prompt(self) -> AnyFormattedText:
        """In prompt.

        :rtype: AnyFormattedText
        """
        # self.formats, self.styles = ansi2prompt_toolkit(str(sys.ps1))
        return [
            ("class:in", "In ["),
            (
                "class:in.number",
                f"{self.python_input.current_statement_index}",
            ),
            ("class:in", "]: "),
        ]
