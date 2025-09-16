r"""Term info
=============

Convert rime/prompt-toolkit.

Rime uses a key code and a key mask to describe a key. Such as: ``(32, 5)``,
means ``Control(4) + Shift(1) + space(32)``.

However, prompt-toolkit uses ``list[Keys | str]``. ``Keys`` is a ``Enum``. such
as ``[tab, "A"]``, ``KEY_ALIASES.get('tab', 'tab')`` will return
``Keys.ControlI``, means ``Control + I, Shift + A``.

Rime supports more keys, such as ``CapsLock``. Prompt-toolkit supports input
many keys at same time, such as ``Control + I, Shift + A``. We only support
their intersection.
"""

import json
import os
from dataclasses import dataclass
from enum import Enum, Flag, unique
from typing import Self

from prompt_toolkit.keys import KEY_ALIASES, Keys

json_dir = os.path.join(os.path.dirname(__file__), "assets", "json")
with open(os.path.join(json_dir, "keys.json")) as f:
    key_map: dict[str, int] = json.load(f)
with open(os.path.join(json_dir, "modifiers.json")) as f:
    modifiers: list = json.load(f)
# escape numbers
key_map = {
    ("_" if k in "".join(map(str, range(10))) else "") + k: v
    for k, v in key_map.items()
}
name_map = {
    "space": " ",
    "enter": "Return",
    "backspace": "BackSpace",
    "pageup": "Page_Up",
    "pagedown": "Page_Down",
}
template_map = {
    "Return": "\x1b[27;{};13~",
}


class BasicKeyEnum(Enum):
    r"""BasickeyEnum."""

    @property
    def rime_name(self) -> str:
        r"""Rime name.

        :rtype: str
        """
        return self.value_to_rime(self.value)

    @property
    def pt_name(self) -> str:
        r"""Prompt toolkit name.

        :rtype: str
        """
        return self.rime_to_pt(self.rime_name)

    @property
    def template(self) -> str | None:
        r"""Template.

        :rtype: str | None
        """
        return template_map.get(self.rime_name)

    @classmethod
    def from_rime_name(cls, name: str) -> Self:
        r"""From rime name. Add escaped '_' for numbers because variable name
        cannot start with number.

        :param name:
        :type name: str
        :rtype: Self
        """
        return cls(
            key_map[
                ("_" if name in "".join(map(str, range(10))) else "") + name
            ]
        )

    @classmethod
    def from_pt_name(cls, name: str) -> Self:
        r"""From pt name.

        :param name:
        :type name: str
        :rtype: Self
        """
        name = cls.pt_to_rime(name)
        return cls.from_rime_name(name)

    @classmethod
    def from_template(cls, template: str) -> Self:
        r"""From template.

        :param template:
        :type template: str
        :rtype: Self
        """
        name = {v: k for k, v in template_map.items()}[template]
        return cls.from_rime_name(name)

    @classmethod
    def new(cls, name_or_template: str) -> Self:
        r"""New.

        :param name_or_template:
        :type name_or_template: str
        :rtype: Self
        """
        if "{}" in name_or_template:
            return cls.from_template(name_or_template)
        elif name_or_template[0].isupper():
            return cls.from_rime_name(name_or_template)
        return cls.from_pt_name(name_or_template)

    @staticmethod
    def rime_to_pt(name: str) -> str:
        r"""Convert rime name to prompt_toolkit name.

        :param name:
        :type name: str
        :rtype: str
        """
        name = {v: k for k, v in name_map.items()}.get(
            name, name if len(name) == 1 else name.lower()
        )
        return name

    @classmethod
    def pt_to_rime(cls, name: str) -> str:
        r"""Convert prompt toolkit name to rime name.

        :param cls:
        :param name:
        :type name: str
        :rtype: str
        """
        name = name_map.get(
            name, name if len(name) == 1 else name.capitalize()
        )
        if name in key_map:
            return name
        return cls.value_to_rime(ord(name))

    @staticmethod
    def value_to_rime(value: int) -> str:
        r"""Value to rime. Remove escaped '_'.
        2 cases will result in ``name not in key_map``:
        1. name: '0', key_map's name: '_0'
        2. name: '=', key_map's name: 'equal'

        :param value:
        :type value: int
        :rtype: str
        """
        return {v: k for k, v in key_map.items()}[value].lstrip("_")


BasicKey = BasicKeyEnum("BasicKey", key_map)


@unique
class ModifierKey(Flag):
    r"""Not all rime modifier (Lock, ...) are supported in terminfo."""

    NULL = 0
    Shift = 2 ** modifiers.index("Shift")
    Alt = 2 ** modifiers.index("Alt")
    Control = 2 ** modifiers.index("Control")

    def get_ansi(self) -> int:
        r"""Get value for ansi escape code.

        :param self:
        :rtype: int
        """
        d = {v: i for i, v in enumerate(self.__class__.__members__.values())}
        ansi = 1
        for flag in self:
            ansi += 2 ** (d[flag] - 1)
        return ansi

    @classmethod
    def from_ansi(cls, ansi: int) -> Self:
        r"""From ansi.

        :param cls:
        :param ansi:
        :type ansi: int
        :rtype: Self
        """
        d = {i: v for i, v in enumerate(cls.__members__.values())}
        _, _, num = bin(ansi - 1).partition("0b")
        value = cls.NULL
        for n, char in enumerate(list(num)):
            if char == "1":
                value |= d[len(d) - 1 - n]
        return value

    def format(self, template: str) -> str:
        r"""Format.

        :param template:
        :type template: str
        :rtype: str
        """
        return template.format(self.get_ansi())


@dataclass
class Key:
    r"""Key."""

    basic: BasicKey = BasicKey.space  # type: ignore
    modifier: ModifierKey = ModifierKey.NULL

    @property
    def code(self) -> int:
        r"""rime key code.

        :param self:
        :rtype: int
        """
        return self.basic.value

    @property
    def mask(self) -> int:
        r"""rime key code.

        :param self:
        :rtype: int
        """
        return self.modifier.value

    @property
    def keys(self) -> tuple[Keys | str, ...]:
        r"""Get prompt-toolkit key name.

        :param self:
        :rtype: tuple[Keys | str, ...]
        """
        keys = []
        template = self.basic.template
        if template:
            keys = list(self.modifier.format(template))
            if keys[0] == "\x1b":
                keys[0] = "escape"
        else:
            name = self.basic.pt_name
            for modifier in self.modifier:
                if modifier == ModifierKey.Alt:
                    keys += ["escape"]
                elif modifier == ModifierKey.Shift:
                    name = "s-" + name
                elif modifier == ModifierKey.Control:
                    name = "c-" + name
        return tuple(keys)

    @classmethod
    def new(
        cls,
        code_or_keys: int | str | tuple[Keys | str, ...],
        modifier: ModifierKey = ModifierKey.NULL,
    ) -> Self:
        r"""New.

        :param cls:
        :param code_or_keys:
        :type code_or_keys: int | str | tuple[Keys | str, ...]
        :param modifier:
        :type modifier: ModifierKey
        :rtype: Self
        """
        if isinstance(code_or_keys, tuple):
            return cls.from_prompt_toolkit(*code_or_keys)
        else:
            if isinstance(code_or_keys, int):
                basic = BasicKey(code_or_keys)
            else:
                basic = BasicKey.new(code_or_keys)
            return cls(basic, modifier)

    @classmethod
    def from_rime(cls, code: int, mask: int) -> Self:
        r"""Create a new Key from rime key code and mask.

        :param cls:
        :param code:
        :type code: int
        :param mask:
        :type mask: int
        :rtype: Self
        """
        return cls(BasicKey(code), ModifierKey(mask))

    @classmethod
    def from_prompt_toolkit(cls, *keys: Keys | str) -> Self:
        r"""Create a new Key from prompt-toolkit key name.

        :param cls:
        :param keys:
        :type keys: Keys | str
        :rtype: Self
        """
        names: list[str] = []
        modifier = ModifierKey.NULL
        for key in keys:
            if key == "escape":
                if len(keys) == 2:
                    modifier |= ModifierKey.Alt
                else:
                    names += ["\x1b"]
            else:
                names += [key]
        if len(names) == 0:
            raise NotImplementedError
        name = "".join(names)
        if len(names) == 1:
            # use tab not c-i
            name = {v: k for k, v in KEY_ALIASES.items()}.get(name, name)
            # get prompt toolkit name
            if name.startswith("c-"):
                modifier |= ModifierKey.Control
                _, _, name = name.partition("c-")
                # extra key aliases
                name = {"^": "6", "-": "_"}.get(name, name)
            if name.startswith("s-"):
                modifier |= ModifierKey.Shift
                _, _, name = name.partition("s-")
        else:
            prefix, _, suffix = name.partition(";")
            modifier |= ModifierKey.from_ansi(int(suffix[0]))
            # get template
            name = prefix + _ + "{}" + suffix[1:]
        basic = BasicKey.new(name)
        return cls(basic, modifier)
