r"""Smartinput
==============

Add spaces around operators.

Refer `vim-smartinput <https://github.com/kana/vim-smartinput>`_.

"""

from typing import TYPE_CHECKING

from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent

if TYPE_CHECKING:
    from ..ime import IME


def load_smartinput_bindings(rime: "IME") -> KeyBindings:
    r"""Smartinput.

    :param rime:
    :type rime: IME
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    # Operation
    @handle(",", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char == " ":
            b.insert_text(",")
        else:
            b.insert_text(", ")

    @handle("+", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.current_char == " ":
            b.insert_text("+")
        else:
            b.insert_text(" + ")

    @handle("@", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if (
            b.document.char_before_cursor == " "
            or b.document.cursor_position_col == 0
        ):
            b.insert_text("@")
        else:
            b.insert_text(" @ ")

    @handle("*", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("*")
        else:
            b.insert_text(" * ")

    @handle("*", "*", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("**")
        else:
            b.insert_text(" ** ")

    @handle("/", "/", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("//")
        else:
            b.insert_text(" // ")

    @handle("%", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if (
            b.document.char_before_cursor == " "
            or b.document.cursor_position_col == 0
        ):
            b.insert_text("%")
        else:
            b.insert_text(" % ")

    @handle("&", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("&")
        else:
            b.insert_text(" & ")

    @handle("|", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("|")
        else:
            b.insert_text(" | ")

    @handle("^", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("^")
        else:
            b.insert_text(" ^ ")

    @handle("<", "<", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<<")
        else:
            b.insert_text(" << ")

    @handle(">", ">", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">>")
        else:
            b.insert_text(" >> ")

    # Relation
    @handle("<", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<")
        else:
            b.insert_text(" < ")

    @handle(">", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">")
        else:
            b.insert_text(" > ")

    @handle(":", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(":=")
        else:
            b.insert_text(" := ")

    @handle("=", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("==")
        else:
            b.insert_text(" == ")

    @handle("!", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("!=")
        else:
            b.insert_text(" != ")

    @handle("<", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<=")
        else:
            b.insert_text(" <= ")

    @handle(">", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">=")
        else:
            b.insert_text(" >= ")

    # Assign
    @handle("=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("=")
        else:
            b.insert_text(" = ")

    @handle("+", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("+=")
        else:
            b.insert_text(" += ")

    @handle("-", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("-=")
        else:
            b.insert_text(" -= ")

    @handle("@", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("@=")
        else:
            b.insert_text(" @= ")

    @handle("*", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("*=")
        else:
            b.insert_text(" *= ")

    @handle("/", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("/=")
        else:
            b.insert_text(" /= ")

    @handle("*", "*", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("**=")
        else:
            b.insert_text(" **= ")

    @handle("/", "/", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("//=")
        else:
            b.insert_text(" //= ")

    @handle("%", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("%=")
        else:
            b.insert_text(" %= ")

    @handle("&", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("&=")
        else:
            b.insert_text(" &= ")

    @handle("|", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("|=")
        else:
            b.insert_text(" |= ")

    @handle("^", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("^=")
        else:
            b.insert_text(" ^= ")

    @handle("<", "<", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text("<<=")
        else:
            b.insert_text(" <<= ")

    @handle(">", ">", "=", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        if b.document.char_before_cursor == " ":
            b.insert_text(">>=")
        else:
            b.insert_text(" >>= ")

    return key_bindings
