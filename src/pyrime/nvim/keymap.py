r"""Keymap
==========

Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/nvim/keymap.lua>
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from pynvim.api.common import RemoteApi

NOWAIT: tuple[str, ...] = ("!", "<Bar>", "}", "~")
# "
for i in 0x23, 0x26:
    key = chr(i)
    NOWAIT += (key,)
# '()
for i in 0x2A, 0x7B:
    key = chr(i)
    NOWAIT += (key,)

SPECIAL: tuple[str, ...] = (
    "<S-Esc>",
    "<S-Tab>",
    "<BS>",
    "<M-BS>",
    "<C-Space>",
    "<M-C-Space>",
    "<M-Bar>",
)
for name in (
    "Insert",
    "CR",
    "Del",
    "Up",
    "Down",
    "Left",
    "Right",
    "Home",
    "End",
    "PageUp",
    "PageDown",
):
    for s_name in (name, "S-" + name):
        for c_s_name in (s_name, "C-" + s_name):
            for keyname in (c_s_name, "M-" + c_s_name):
                SPECIAL += ("<" + keyname + ">",)
for i in range(1, 35):
    SPECIAL += (f"<F{i}>",)
for i in 0x41, 0x5A:
    keyname = chr(i)
    for lhs in (f"<C-{keyname}>", f"<M-C-{keyname}>"):
        SPECIAL += (lhs,)
SPECIAL += ("<M-C-[>",)
for i in 0x5C, 0x5F:
    keyname = chr(i)
    for lhs in (f"<C-{keyname}>", f"<M-C-{keyname}>"):
        SPECIAL += (lhs,)


@dataclass
class Keymap:
    r"""Keymap."""

    api: RemoteApi
    nowait: tuple[str, ...] = NOWAIT
    special: tuple[str, ...] = SPECIAL
    disable: tuple[str, ...] = ("<Space>",)
    maps: dict[str, str] = field(default_factory=dict)

    def set(
        self, lhs: str, callback: str | None | Callable[[str], str]
    ) -> None:
        r"""Set.

        :param lhs:
        :type lhs: str
        :param callback:
        :type callback: str | None | Callable[[str], str]
        :rtype: None
        """
        if callback is None and lhs in self.maps:
            self.api.del_keymap("i", lhs)
            del self.maps[lhs]
        elif callback and lhs not in self.maps:
            rhs = callback if isinstance(callback, str) else callback(lhs)
            self.api.set_keymap("i", lhs, rhs, {})
            self.maps[lhs] = rhs

    def set_special(self, callback: None | Callable[[str], str]) -> None:
        r"""Set special.

        :param callback:
        :type callback: None | Callable[[str], str]
        :rtype: None
        """
        for lhs in self.special:
            self.set(lhs, callback)

    def set_nowait(self, is_enabled: bool) -> None:
        r"""Set nowait.

        :param is_enabled:
        :type is_enabled: bool
        :rtype: None
        """
        for lhs in self.nowait:
            self.set(lhs, lhs if is_enabled else None)
