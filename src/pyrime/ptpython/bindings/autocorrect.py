r"""Autocorrect
===============

Custom key binding for some simple autocorrection while typing.
conflict with vi block insert mode
"""

from typing import TYPE_CHECKING

from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent

if TYPE_CHECKING:
    from ..ime import IME


def load_autocorrect_bindings(
    rime: "IME", corrections: dict[str, str]
) -> KeyBindings:
    r"""Load autocorrect bindings.

    :param rime:
    :type rime: IME
    :param corrections:
    :type corrections: dict[str, str]
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    @handle(" ", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        "When a space is pressed. Check & correct word before cursor."
        b = event.cli.current_buffer
        w = b.document.get_word_before_cursor()

        if w is not None and w in corrections:
            b.delete_before_cursor(count=len(w))
            b.insert_text(corrections[w])

        b.insert_text(" ")

    return key_bindings
