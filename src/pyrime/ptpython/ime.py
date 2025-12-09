r"""Rime for Prompt Toolkit
===========================

"""

from collections.abc import Callable
from dataclasses import dataclass, field

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters.app import emacs_insert_mode, vi_insert_mode
from prompt_toolkit.filters.base import Condition, Filter
from prompt_toolkit.formatted_text.base import AnyFormattedText
from prompt_toolkit.key_binding.key_bindings import (
    KeyBindingsBase,
    merge_key_bindings,
)
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
from ..rime import RimeBase
from .bindings import load_key_bindings


@dataclass
class IME(RimeBase):
    r"""Rime for prompt toolkit."""

    app: Application = field(default_factory=get_app)
    get_input_prompt: Callable[[], AnyFormattedText] = lambda: ""
    key_bindings: KeyBindingsBase | None = None
    content: BufferControl = field(default_factory=BufferControl)
    iminsert: bool = False

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.window = Window(self.content)
        self.float = Float(Frame(self.window))
        self.float.left, self.float.top = self.calculate()
        self.layout = Layout(
            FloatContainer(
                self.app.layout.container,
                [self.float],
            )
        )

        if self.key_bindings is None:
            self.key_bindings = load_key_bindings(self)
        self.app.key_bindings = merge_key_bindings(
            ([self.app.key_bindings] if self.app.key_bindings else [])
            + [self.key_bindings]
        )

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
        # insert text before calculating cursor position
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

    @staticmethod
    def calculate_buffer(buffer: Buffer) -> tuple[int, int]:
        r"""Calculate buffer.

        :param buffer:
        :type buffer: Buffer
        :rtype: tuple[int, int]
        """
        lines = buffer.text[: buffer.cursor_position].splitlines()
        top = len(lines)
        left = wcswidth(lines[-1]) if top > 0 else 0
        return left, top

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
        buffer = self.app.layout.current_buffer
        left, top = self.calculate_buffer(buffer) if buffer else (0, 0)
        formatted_text = self.get_input_prompt()
        left += wcswidth(self.stringifyAnyFormattedText(formatted_text))
        return left, top

    @property
    def is_enabled(self) -> bool:
        r"""Is enabled.

        :rtype: bool
        """
        return super().is_enabled

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        r"""Is enabled.

        :param enabled:
        :type enabled: bool
        :rtype: None
        """
        if (
            super().is_enabled == enabled
            or not (emacs_insert_mode | vi_insert_mode)()
        ):
            return
        self.layout, self.app.layout = (
            self.app.layout,
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

    @property
    def has_preedit(self) -> bool:
        r"""Has preedit.

        :rtype: bool
        """
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

    def keys_available(self, keys) -> Filter:
        r"""Filter.

        :param keys:
        :type keys: tuple[Keys | str, ...]
        :rtype: Filter
        """

        return (
            self.keys_is_a_char(keys) & self.rime_available
        ) | self.preedit_available
