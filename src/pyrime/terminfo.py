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
key_map = {
    ("_" if k in "".join(map(str, range(10))) else "") + k: v
    for k, v in key_map.items()
}
name_map = {
    "Enter": "Return",
    "Pageup": "Page_Up",
    "Pagedown": "Page_Down",
}
template_map = {
    "Return": "\x1b[27;{};13~",
}


class BasicKeyEnum(Enum):
    r"""BasickeyEnum."""

    def get_rime_name(self) -> str:
        r"""Get rime name.

        :rtype: str
        """
        return {v: k for k, v in key_map.items()}[self.value].lstrip("_")

    def get_pt_name(self) -> str:
        r"""Get pt name.

        :rtype: str
        """
        return self.rime_to_pt(self.get_rime_name())

    def get_template(self) -> str | None:
        r"""Get template.

        :rtype: str | None
        """
        return template_map.get(self.get_rime_name())

    @classmethod
    def from_rime_name(cls, name: str) -> Self:
        r"""From rime name.

        :param name:
        :type name: str
        :rtype: Self
        """
        return cls(key_map[name])

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
        if len(name) == 1:
            return name
        name = {v: k for k, v in name_map.items()}.get(name, name)
        name = name.lower()
        return name

    @staticmethod
    def pt_to_rime(name: str) -> str:
        r"""Convert prompt_toolkit name to rime name.

        :param name:
        :type name: str
        :rtype: str
        """
        if name == " ":
            return "space"
        if len(name) == 1:
            return name
        name = name.capitalize()
        name = name_map.get(name, name)
        if name in key_map:
            return name
        raise NotImplementedError


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

    basic: BasicKey
    modifier: ModifierKey

    def get_rime(self) -> tuple[int, int]:
        r"""Get rime key code and mask.

        :param self:
        :rtype: tuple[int, int]
        """
        return self.basic.value, self.modifier.value

    @classmethod
    def new(
        cls,
        code_or_keys: int | str | list[Keys | str],
        modifier: ModifierKey = ModifierKey.NULL,
    ) -> Self:
        r"""New.

        :param cls:
        :param code_or_keys:
        :type code_or_keys: int | str | list[Keys | str]
        :param modifier:
        :type modifier: ModifierKey
        :rtype: Self
        """
        if isinstance(code_or_keys, list):
            return cls.from_prompt_toolkit(code_or_keys)
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

    def get_prompt_toolkit(self) -> list[Keys | str]:
        r"""Get prompt-toolkit key name.

        :param self:
        :rtype: list[Keys | str]
        """
        keys = []
        template = self.basic.get_template()
        if template:
            keys = list(self.modifier.format(template))
            if keys[0] == "\x1b":
                keys[0] = "escape"
        else:
            name = self.basic.get_pt_name()
            for modifier in self.modifier:
                if modifier == ModifierKey.Alt:
                    keys += ["escape"]
                elif modifier == ModifierKey.Shift:
                    name = "s-" + name
                elif modifier == ModifierKey.Control:
                    name = "c-" + name
        return keys

    @classmethod
    def from_prompt_toolkit(cls, keys: list[Keys | str]) -> Self:
        r"""Create a new Key from prompt-toolkit key name.

        :param cls:
        :param keys:
        :type keys: list[Keys | str]
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
            name = {v: k for k, v in KEY_ALIASES.items()}.get(name, name)
            if name.startswith("c-"):
                modifier |= ModifierKey.Control
                _, _, name = name.partition("c-")
                name = {"^": "6", "-": "_"}.get(name, name)
            if name.startswith("s-"):
                modifier |= ModifierKey.Shift
                _, _, name = name.partition("s-")
            basic = BasicKey.new(name)
        else:
            prefix, _, suffix = name.partition(";")
            modifier |= ModifierKey.from_ansi(int(suffix[0]))
            name = prefix + _ + "{}" + suffix[1:]
            basic = BasicKey.new(name)
        return cls(basic, modifier)
