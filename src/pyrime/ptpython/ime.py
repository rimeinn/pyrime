r"""Rime for Prompt Toolkit
===========================

"""

from collections.abc import Callable
from dataclasses import dataclass, field

from prompt_toolkit.filters.app import emacs_insert_mode, vi_insert_mode
from prompt_toolkit.filters.base import Condition, Filter
from prompt_toolkit.key_binding.key_bindings import merge_key_bindings
from prompt_toolkit.keys import Keys

from ..key import Key
from ..rime import RimeBase
from .bindings import load_key_bindings
from .layout import RimeLayout


@dataclass
class _IME:
    layout: RimeLayout = field(default_factory=RimeLayout)


@dataclass
class IME(RimeBase, _IME):
    r"""Rime for prompt toolkit."""

    iminsert: bool = False

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.back_layout = self.layout
        self.app = self.layout.app
        self.app.key_bindings = merge_key_bindings(
            ([self.app.key_bindings] if self.app.key_bindings else [])
            + [load_key_bindings(self)]
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
        self.layout.update(lines, col)

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
        self.back_layout, self.app.layout = self.app.layout, self.back_layout
        self.layout.update()
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
        return self.layout.window.height == 2

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
