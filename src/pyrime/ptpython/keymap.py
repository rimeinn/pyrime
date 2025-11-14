r"""Keys
========

Provide ``KEYS`` for key bindings.
"""

from ..key import Key, ModifierKey

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
