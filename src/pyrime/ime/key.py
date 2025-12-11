r"""Key
=======

Refer <https://github.com/rimeinn/rime.nvim/blob/0.2.12/packages/ime/lua/ime/key.lua>
"""

from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import Any, ClassVar, Self


@dataclass
class KeyBase(ABC):
    r"""Key.

    For rime or fcitx key, we pass ``key_map`` and ``shift``, ``control``,
    ``alt``.
    provide a factory method ``new()`` to create an instance from vim key name.

    basic name use lower, modifier name use upper first character.
    """

    basic: int
    modifier: int
    aliases: ClassVar[dict[str, str]] = {
        "<nul>": "<c-space>",
        "<c-@>": "<c-space>",
        "<c-h>": "<bs>",
        "<c-i>": "<tab>",
        "<nl>": "<c-j>",
        "<c-m>": "<return>",
        "<enter>": "<return>",
        "<cr>": "<return>",
        "<c-[>": "<esc>",
        "<space>": " ",
        "<lt>": "<",
        "<bslash>": "\\",
        "<bar>": "|",
    }

    def __str__(self):
        r"""For GUI. if no modifier and basic is printable, print basic."""
        if self.modifier > 0:
            return ""
        char = chr(self.basic)
        return char if char.isprintable() else ""

    def __iter__(self) -> Generator[int, Any, None]:
        yield int(self.basic)
        yield int(self.modifier)

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.basic = self.basic_enum(self.basic)
        self.modifier = self.modifier_flag(self.modifier)

    def __init_subclass__(
        cls, key_map: dict[str, int], shift: int, alt: int, control: int
    ) -> None:
        r"""Init subclass.

        :param cls:
        :param key_map:
        :type key_map: dict[str, int]
        :param shift:
        :type shift: int
        :param alt:
        :type alt: int
        :param control:
        :type control: int
        :rtype: None
        """
        super().__init_subclass__()
        keys = {
            ("_" if k in "".join(map(str, range(10))) else "") + k: v
            for k, v in key_map.items()
        }
        cls.basic_enum = IntEnum("Basic", keys)
        cls.modifier_flag = IntFlag(
            "Modifier",
            {"S": 2**shift, "A": 2**alt, "M": 2**alt, "C": 2**control},
        )

    @classmethod
    def new(cls, name: str) -> Self:
        r"""Create a Key from vim name.

        :param name: '<Esc>', 'a', ...
        :type name: str
        :rtype: Self
        """
        name = cls.aliases.get(name.lower(), name)
        if not (name.startswith("<") and name.endswith(">")):
            try:
                return cls(ord(name), 0)
            except TypeError as e:
                raise NotImplementedError(
                    f"{len(name)} keys are not implemented"
                ) from e
        modifier = 0
        name = name[1:-1]
        prefix, _, name = name.rpartition("-")
        while prefix:
            try:
                modifier |= getattr(cls.modifier_flag, prefix.upper())
            except AttributeError as e:
                raise NotImplementedError(
                    f"modifier {prefix} is not implemented"
                ) from e
            prefix, _, name = name.rpartition("-")
        # make "-" work
        name = _ + name
        # C-A is same as c-a
        if modifier == cls.modifier_flag.C:
            name = name.lower()
        if len(name) == 1:
            return cls(ord(name), modifier)
        name = name.lower()
        # space -> ' '
        basic = cls.convert(cls.aliases.get(f"<{name}>", name))
        return cls(basic, modifier)

    @classmethod
    @abstractmethod
    def convert(cls, name: str) -> int:
        r"""Convert a vim special basic key to ``basic_enum``.

        :param name: 'ESC', 'TAB'
        :type name: str
        :rtype: int
        """
