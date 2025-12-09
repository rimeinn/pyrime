r"""Formatted Text
==================
"""

from collections.abc import Callable

from prompt_toolkit.formatted_text.base import AnyFormattedText


class formatted_text(str):
    r"""Formatted text."""

    def __new__(cls, any_formatted_text: AnyFormattedText) -> str:
        r"""Stringify any formatted text.

        :param cls:
        :param any_formatted_text:
        :type any_formatted_text: AnyFormattedText
        :rtype: str
        """
        text = getattr(
            any_formatted_text, "__pt_formatted_text__", any_formatted_text
        )
        if isinstance(text, Callable):
            text = text()

        if isinstance(text, list):
            text = "".join(text for _, text, *_ in text)
        if isinstance(text, str):
            return text
        return ""
