r"""Rime for Ptpython
=====================

``RIME`` inherits ``pyrime.ptpython``'s ``IME`` to use ``Session``s OOP APIs to
call librime on the basis of ``IME``.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from prompt_toolkit.filters.app import emacs_insert_mode, vi_insert_mode
from prompt_toolkit.filters.base import Condition, Filter
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
from ptpython.repl import PythonRepl
from wcwidth import wcswidth

from ..key import Key
from ..rime import RimeBase
from .keymap import KEYS


@dataclass
class IME:
    r"""An empty class to make repl as first argument of ``__init__()``"""

    repl: PythonRepl


@dataclass
class Rime(RimeBase, IME):
    r"""Rime for ptpython."""

    keys_set: tuple[tuple[Keys | str, ...], ...] = KEYS
    content: BufferControl = field(default_factory=BufferControl)
    iminsert: bool = False

    @property
    def has_preedit(self) -> bool:
        return self.window.height == 2

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

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
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

            @self.repl.add_key_binding(*keys, filter=self.keys_available(keys))
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
        formatted_text = self.repl.get_input_prompt()
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
        if (
            super().is_enabled == enabled
            or not (emacs_insert_mode | vi_insert_mode)()
        ):
            return
        self.iminsert = self.is_enabled
        self.layout, self.repl.app.layout = (
            self.repl.app.layout,
            self.layout,
        )
        fset = RimeBase.is_enabled.fset
        if fset:
            fset(self, enabled)

    @property
    def rime_available(self) -> Condition:
        r"""Filter. Only when ``preedit`` is not available, key binding works.

        :rtype: Filter
        """

        @Condition
        def _() -> bool:
            r""".

            :rtype: bool
            """
            return self.is_enabled

        return _

    @staticmethod
    def keys_is_a_char(keys: tuple[Keys | str, ...]) -> Condition:
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
            return len(keys) == 1 == len(keys[0])

        return _

    def keys_available(self, keys) -> Filter:
        r"""Filter.

        :param keys:
        :type keys: tuple[Keys | str, ...]
        :rtype: Filter
        """

        return (
            self.keys_is_a_char(keys) & self.rime_available
        ) | self.preedit_available
