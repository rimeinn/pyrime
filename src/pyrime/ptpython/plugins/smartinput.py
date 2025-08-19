r"""Smartinput
==============

Add spaces around operators.

Refer `vim-smartinput <https://github.com/kana/vim-smartinput>`_.
"""

from prompt_toolkit.key_binding.key_processor import KeyPressEvent

from ..utils.condition import InsertMode
from . import RimeBase


def smartinput(rime: RimeBase) -> None:
    r"""Smartinput.

    :param rime:
    :type rime: Rime
    :rtype: None
    """
    repl = rime.repl

    # One {{{1 #
    @repl.add_key_binding(",", filter=rime.filter(InsertMode))  # type: ignore
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

    # 1}}} One #

    # Two {{{1 #
    # Operation {{{2 #
    @repl.add_key_binding("+", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("@", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("*", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("*", "*", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("/", "/", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("%", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("&", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("|", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("^", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("<", "<", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding(">", ">", filter=rime.filter(InsertMode))  # type: ignore
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

    # 1}}} Operation #

    # Relation {{{2 #
    @repl.add_key_binding("<", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding(">", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding(":", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("=", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("!", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("<", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding(">", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    # 1}}} Relation #

    # Assign {{{2 #
    @repl.add_key_binding("=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("+", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("-", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("@", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("*", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("/", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("*", "*", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("/", "/", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("%", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("&", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("|", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("^", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding("<", "<", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    @repl.add_key_binding(">", ">", "=", filter=rime.filter(InsertMode))  # type: ignore
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

    # 2}}} Assign #
    # 1}}} Two #


# ex: foldmethod=marker
