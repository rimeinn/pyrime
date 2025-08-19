r"""Autopair
============

Refer `zsh-autopair <https://github.com/hlissner/zsh-autopair>`_.
"""

from prompt_toolkit.key_binding.bindings.named_commands import (
    backward_char,
    backward_delete_char,
    delete_char,
    forward_char,
)
from prompt_toolkit.key_binding.key_processor import KeyPressEvent

from ..utils.condition import InsertMode
from . import RimeBase


def autopair(rime: RimeBase) -> None:
    r"""Autopair.

    :param rime:
    :type rime: Rime
    :rtype: None
    """
    repl = rime.repl

    @repl.add_key_binding("c-h", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("[", filter=rime.filter(InsertMode))  # type: ignore
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("[]")
        backward_char(event)

    @repl.add_key_binding("]", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("(", filter=rime.filter(InsertMode))  # type: ignore
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("()")
        backward_char(event)

    @repl.add_key_binding(")", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("{", filter=rime.filter(InsertMode))  # type: ignore
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.cli.current_buffer.insert_text("{}")
        backward_char(event)

    @repl.add_key_binding("}", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("'", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("`", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding('"', filter=rime.filter(InsertMode))  # type: ignore
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
