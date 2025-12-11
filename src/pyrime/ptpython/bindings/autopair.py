r"""Autopair
============

Refer `zsh-autopair <https://github.com/hlissner/zsh-autopair>`_.
"""

from typing import TYPE_CHECKING

from prompt_toolkit.key_binding.bindings.named_commands import (
    backward_char,
    backward_delete_char,
    delete_char,
    forward_char,
)
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys

if TYPE_CHECKING:
    from ..ime import IME


def load_autopair_bindings(rime: "IME") -> KeyBindings:
    r"""Autopair.

    :param rime:
    :type rime: IME
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    @handle(Keys.Backspace, filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        cr: str = b.document.current_char
        if b.document.cursor_position_col == 0:
            cl: str = ""
        else:
            cl: str = b.document.char_before_cursor
        if b.document.cursor_position_col <= 1:
            cl2: str = ""
        else:
            backward_char(event)
            cl2: str = b.document.char_before_cursor
            forward_char(event)
        for c0, c1 in ["[]", "()", "{}", "''", "``", '""']:
            if cl == c0 and cr == c1:
                delete_char(event)
                break
            elif cl == c1 and cl2 == c0:
                backward_delete_char(event)
                break
        backward_delete_char(event)

    @handle("[", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("[]")
        backward_char(event)

    @handle("]", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != "]":
            b.insert_text("]")
        else:
            forward_char(event)

    @handle("(", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("()")
        backward_char(event)

    @handle(")", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != ")":
            b.insert_text(")")
        else:
            forward_char(event)

    @handle("{", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("{}")
        backward_char(event)

    @handle("}", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != "}":
            b.insert_text("}")
        else:
            forward_char(event)

    @handle("'", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != "'":
            b.insert_text("''")
            backward_char(event)
        else:
            forward_char(event)

    @handle("`", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != "`":
            b.insert_text("``")
            backward_char(event)
        else:
            forward_char(event)

    @handle('"', filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char != '"':
            b.insert_text('""')
            backward_char(event)
        else:
            forward_char(event)

    return key_bindings
