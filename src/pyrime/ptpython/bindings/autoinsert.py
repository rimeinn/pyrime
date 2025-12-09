r"""Autoinsert
==============
"""

from typing import TYPE_CHECKING

from prompt_toolkit.filters.app import vi_navigation_mode
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent

if TYPE_CHECKING:
    from ..ime import IME


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


def load_autoinsert_bindings(rime: "IME") -> KeyBindings:
    r"""Load autoinsert bindings.

    :param rime:
    :type rime: IME
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    @handle("K", filter=vi_navigation_mode & ~rime.preedit_available)
    @handle("c-x", "c-h", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "help(", ")")

    @handle("c-x", "c-p", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "print(", ")")

    @handle("c-x", "c-_", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, 'import numpy as np; np.lookfor("', '")')

    @handle("c-x", "c-o", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, 'import numpy as np; np.source("', '")')

    @handle("c-x", "c-l", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "list(", ")")

    @handle("c-x", "c-d", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "dict(", ")")

    @handle("c-x", "c-t", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "type(", ")")

    @handle("c-x", "c-n", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "next(iter(", "))")

    @handle("c-x", "c-space", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        insert(event, "len(", ")")

    @handle("c-x", "c-b", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """Add custom key binding for PDB.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("\nbreakpoint()\n")

    return key_bindings
