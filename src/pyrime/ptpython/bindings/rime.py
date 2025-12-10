r"""Rime
========

Refer
`<https://github.com/prompt-toolkit/python-prompt-toolkit/blob/3.0.52/src/prompt_toolkit/key_binding/bindings/basic.py#L42>`_
"""

from typing import TYPE_CHECKING

from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import ALL_KEYS, Keys

from ...key import Key

if TYPE_CHECKING:
    from ..ime import IME


class pt_key_name(str):
    r"""Prompt toolkit key name."""

    pt_to_vim: dict[Keys | str, str] = {
        Keys.Escape: "esc",
        Keys.Delete: "del",
    }

    def __new__(cls, keys: tuple[Keys | str, ...]) -> str:
        r"""New.

        :param cls:
        :param keys:
        :type keys: tuple[Keys | str, ...]
        :rtype: str
        """
        if len(keys) > 2 or len(keys) == 0:
            raise NotImplementedError(f"{keys} is not (escape, X) or (X,)")
        prefix = ""
        name = keys[0]
        if len(keys) > 1:
            if name == Keys.Escape:
                prefix = "A-"
                name = keys[1]
            else:
                raise NotImplementedError(f"{keys[0]} is not escape")
        _prefix, _, name = name.rpartition("-")
        while _prefix:
            prefix += _prefix + "-"
            _prefix, _, name = name.rpartition("-")
        # make "-" work
        name = _ + name
        if prefix == "":
            return name
        name = cls.pt_to_vim.get(name, name)
        return f"<{prefix + name}>"


ALL_CHARS = tuple(chr(i) for i in range(ord(" "), ord("~") + 1))
EXTRA_KEYS_SET = tuple(tuple(f"\x1b[27;{i};13~") for i in (2, 5, 6, 7, 8))


def load_rime_bindings(
    rime: "IME",
    keys_set: tuple[tuple[Keys | str, ...], ...] = (
        tuple((k,) for k in ALL_KEYS)
        + tuple((Keys.Escape, k) for k in ALL_KEYS if k != Keys.Escape)
        + tuple((k,) for k in ALL_CHARS)
        + tuple((Keys.Escape, k) for k in ALL_CHARS)
    )
    + EXTRA_KEYS_SET,
) -> KeyBindings:
    r"""Load rime bindings.

    :param rime:
    :type rime: IME
    :param keys_set:
    :type keys_set: tuple[tuple[Keys | str, ...], ...]
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    handle = key_bindings.add

    for keys in keys_set:

        @handle(*keys, filter=rime.keys_available(keys))
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
            rime.exe(
                lambda text: event.cli.current_buffer.insert_text(text),
                Key.new(pt_key_name(keys)),
            )

    return key_bindings
