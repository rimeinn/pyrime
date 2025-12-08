r"""Rime
========

Refer
`<https://github.com/prompt-toolkit/python-prompt-toolkit/blob/3.0.52/src/prompt_toolkit/key_binding/bindings/basic.py#L42>`_
"""

from typing import TYPE_CHECKING

from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys

from ...key import Key, ModifierKey

if TYPE_CHECKING:
    from ..rime import Rime

KEYS = {
    ("s-tab",),
    ("s-escape",),
    ("escape", "backspace"),
    ("escape", "enter"),
    Key.new("enter", ModifierKey.Shift).keys,
    Key.new("enter", ModifierKey.Control).keys,
    Key.new("enter", ModifierKey.Shift | ModifierKey.Control).keys,
    Key.new("enter", ModifierKey.Shift | ModifierKey.Alt).keys,
    Key.new("enter", ModifierKey.Control | ModifierKey.Alt).keys,
    Key.new(
        "enter",
        ModifierKey.Shift | ModifierKey.Control | ModifierKey.Alt,
    ).keys,
}
for order in range(ord(" "), ord("~") + 1):
    KEYS |= {(chr(order),)}
for number in range(1, 24):
    KEYS |= {(f"f{number}",)}
for keyname in {
    "insert",
    "delete",
    "up",
    "down",
    "left",
    "right",
    "home",
    "end",
    "pageup",
    "pagedown",
}:
    KEYS |= {
        (keyname,),
        ("c-" + keyname,),
        ("s-" + keyname,),
        ("c-s-" + keyname,),
        ("escape", keyname),
        ("escape", "c-" + keyname),
        ("escape", "s-" + keyname),
        ("escape", "c-s-" + keyname),
    }
for order in range(ord("@"), ord("[")):
    key = "c-" + chr(order).lower()
    KEYS |= {(key,), ("escape", key)}
KEYS |= {("escape", "escape")}
for order in range(ord("[") + 1, ord("_")):
    key = "c-" + chr(order)
    KEYS |= {(key,), ("escape", key)}
for order in range(ord(" "), ord("~") + 1):
    KEYS |= {("escape", chr(order))}
KEYS = tuple(KEYS)


def load_rime_bindings(
    rime: "Rime", keys_set: tuple[tuple[Keys | str, ...], ...] = KEYS
) -> KeyBindings:
    r"""Load rime bindings.

    :param rime:
    :type rime: Rime
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
                Key.new(keys),
            )

    return key_bindings
