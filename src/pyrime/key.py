r"""Key for rime
================

Refer <https://github.com/rimeinn/rime.nvim/blob/0.2.12/lua/rime/key.lua>
"""

import json
import os
from dataclasses import dataclass
from typing import ClassVar

from .ime.key import KeyBase

json_dir = os.path.join(os.path.dirname(__file__), "assets", "json")
with open(os.path.join(json_dir, "keys.json")) as f:
    key_map: dict[str, int] = json.load(f)
with open(os.path.join(json_dir, "modifiers.json")) as f:
    modifiers: list = json.load(f)


@dataclass
class Key(
    KeyBase,
    key_map=key_map,
    shift=modifiers.index("Shift"),
    alt=modifiers.index("Alt"),
    control=modifiers.index("Control"),
):
    r"""Key."""

    aliases: ClassVar[dict[str, str]] = KeyBase.aliases | {
        "<c-^>": "<c-6>",
        "<c-_>": "<c-->",
        "<c-/>": "<c-->",
    }
    vim_to_rime: ClassVar[dict[str, str]] = {
        "pageup": "Page_Up",
        "pagedown": "Page_Down",
        "esc": "Escape",
        "bs": "BackSpace",
        "del": "Delete",
    }

    def __str__(self) -> str:
        r"""Get ANSI escape code.

        :rtype: str
        """
        if self.modifier == 0:
            return chr(self.basic)
        if self.modifier == self.modifier_flag.A:
            return chr(self.basic)
        if self.modifier == self.modifier_flag.C:
            return chr(self.basic)
        return chr(self.basic)

    @classmethod
    def convert(cls, name: str) -> int:
        r"""Convert a vim special basic key to rime's ``basic_enum``.

        :param name: 'ESC', 'TAB', not one character
        :type name: str
        :rtype: int
        """
        return key_map[cls.vim_to_rime.get(name, name.capitalize())]
