r"""Autoinsert
==============
"""

from typing import TYPE_CHECKING

from prompt_toolkit.filters.app import (
    emacs_insert_mode,
    vi_insert_mode,
    vi_navigation_mode,
)
from prompt_toolkit.filters.base import Filter
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys

if TYPE_CHECKING:
    from ..ime import IME

insert_mode = emacs_insert_mode | vi_insert_mode
INSERTIONS = {
    ("help(", ")"): {("K",): vi_navigation_mode, ("c-x", "c-h"): insert_mode},
    ("print(", ")"): {("c-x", "c-p"): insert_mode},
    ('import numpy as np; np.lookfor("', '")'): {("c-x", "c-_"): insert_mode},
    ('import numpy as np; np.source("', '")'): {("c-x", "c-o"): insert_mode},
    ("list(", ")"): {("c-x", "c-l"): insert_mode},
    ("dict(", ")"): {("c-x", "c-d"): insert_mode},
    ("type(", ")"): {("c-x", "c-t"): insert_mode},
    ("next(iter(", "))"): {("c-x", "c-n"): insert_mode},
    ("len(", ")"): {("c-x", "c-space"): insert_mode},
    ("\nbreakpoint()\n", ""): {("c-x", "c-b"): insert_mode},
}


def insert(event: KeyPressEvent, pre: str = "(", post: str = ")") -> None:
    """Insert.

    :param event:
    :type event: KeyPressEvent
    :param pre:
    :type pre: str
    :param post:
    :type post: str
    :rtype: None
    """
    event.current_buffer.cursor_position += (
        event.current_buffer.document.get_start_of_line_position(
            after_whitespace=True
        )
    )
    event.cli.current_buffer.insert_text(pre)
    event.current_buffer.cursor_position += (
        event.current_buffer.document.get_end_of_line_position()
    )
    event.cli.current_buffer.insert_text(post)
    event.current_buffer.validate_and_handle()


def load_autoinsert_bindings(
    rime: "IME",
    insertions: dict[tuple[str, str], dict[tuple[Keys | str, ...], Filter]]
    | None = None,
) -> KeyBindings:
    r"""Load autoinsert bindings.

    :param rime:
    :type rime: IME
    :param insertions:
    :type insertions: tuple[str, str], dict[tuple[Keys | str, ...], Filter]
                    | None
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    handle = key_bindings.add
    if insertions is None:
        insertions = INSERTIONS

    for (pre, post), filters in insertions.items():
        for keys, filter in filters.items():

            @handle(*keys, filter=filter & ~rime.preedit_available)
            def _(
                event: KeyPressEvent, pre: str = pre, post: str = post
            ) -> None:
                """.

                :param event:
                :type event: KeyPressEvent
                :param pre:
                :type pre: str
                :param post:
                :type post: str
                :rtype: None
                """
                insert(event, pre, post)

    return key_bindings
