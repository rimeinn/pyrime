r"""Rime for Ptpython
=====================

``RIME`` inherits ``pyrime.ptpython``'s ``IME`` to use ``Session``s OOP APIs to
call librime on the basis of ``IME``.
"""

from collections.abc import Callable
from dataclasses import dataclass

from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text.base import AnyFormattedText
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame
from wcwidth import wcswidth

from ..key import Key
from ..keys import KEYS
from ..rime import RimeBase
from .ime import IME


@dataclass
class Rime(RimeBase, IME):
    r"""RIME inherit IME."""

    keys_set: tuple[tuple[Keys | str, ...], ...] = KEYS

    @property
    def has_preedit(self) -> bool:
        return self.window.height == 2

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.content = BufferControl()
        self.window = Window(self.content)
        self.float = Float(Frame(self.window))
        self.float.left, self.float.top = self.calculate()
        self.layout = Layout(
            FloatContainer(
                self.repl.app.layout.container,
                [self.float],
            )
        )
        for keys in self.keys_set:

            @self.repl.add_key_binding(*keys, filter=self.mode(keys))
            def _(
                event: KeyPressEvent, keys: tuple[Keys | str, ...] = keys
            ) -> None:
                r""".

                :param event:
                :type event: KeyPressEvent
                :param keys:
                :type keys: tuple[Keys | str, ...]
                :rtype: None
                """
                self.key_binding(event, *keys)

    def mode(self, keys: tuple[Keys | str, ...]) -> Condition:
        r"""Mode.

        :param keys:
        :type keys: tuple[Keys | str, ...]
        :rtype: Condition
        """

        @Condition
        def _(keys: tuple[Keys | str, ...] = keys) -> bool:
            r""".

            :param keys:
            :type keys: tuple[Keys | str, ...]
            :rtype: bool
            """
            if len(keys) == 1 == len(keys[0]):
                return self.is_enabled
            if len(keys) == 1 or len(keys) > 1 and keys[0] == "escape":
                return self.has_preedit
            raise NotImplementedError

        return _

    def exe(self, callback: Callable[[str], None], *keys: Key) -> None:
        r"""Override ``RimeBase``.

        :param self:
        :param callback:
        :type callback: Callable[[str], None]
        :param keys:
        :type keys: Key
        :rtype: None
        """
        text, lines, col = self.draw(*keys)
        callback(text)
        self.content.buffer.text = "\n".join(lines)
        self.window.height = len(lines)
        self.window.width = (
            max(wcswidth(line) for line in lines)
            if self.window.height > 0
            else 0
        )
        self.float.left, self.float.top = self.calculate()
        self.float.left += col

    def key_binding(self, event: KeyPressEvent, *keys: Keys | str) -> None:
        r"""Key binding.

        :param event:
        :type event: KeyPressEvent
        :param keys:
        :type keys: Keys | str
        :rtype: None
        """
        self(
            lambda text: event.cli.current_buffer.insert_text(text),
            Key.new(keys),
        )

    @staticmethod
    def stringifyAnyFormattedText(formatted_text: AnyFormattedText) -> str:
        r"""stringify ``AnyFormattedText``.

        :param formatted_text:
        :type formatted_text: AnyFormattedText
        :rtype: str
        """
        _formatted_text = getattr(
            formatted_text, "__pt_formatted_text__", None
        )
        if _formatted_text:
            formatted_text = _formatted_text
        if isinstance(formatted_text, Callable):
            formatted_text = formatted_text()

        if isinstance(formatted_text, str):
            return formatted_text
        pwcs = ""
        if isinstance(formatted_text, list):
            for _, text, *_ in formatted_text:
                pwcs += text
        return pwcs

    def calculate(self) -> tuple[int, int]:
        r"""Calculate.

        :rtype: tuple[int, int]
        """
        formatted_text = self.repl.all_prompt_styles[
            self.repl.prompt_style
        ].in_prompt()
        left = wcswidth(self.stringifyAnyFormattedText(formatted_text))
        top = 0
        if self.repl.app.layout.current_buffer:
            lines = self.repl.app.layout.current_buffer.text[
                : self.repl.app.layout.current_buffer.cursor_position
            ].splitlines()
            top += len(lines)
            if top > 0:
                left += wcswidth(lines[-1])
        return left, top

    @property
    def is_enabled(self) -> bool:
        return super().is_enabled

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        if super().is_enabled != enabled:
            self.layout, self.repl.app.layout = (
                self.repl.app.layout,
                self.layout,
            )
        fset = RimeBase.is_enabled.fset
        if fset:
            fset(self, enabled)
