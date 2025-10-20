r"""Viemacs
===========

Use ``emacs_insert_mode`` to replace ``vi_insert_mode``

Refer `vim-rsi <https://github.com/tpope/vim-rsi>`_.
"""

from prompt_toolkit.clipboard import ClipboardData
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import (
    in_paste_mode,
)
from prompt_toolkit.filters.app import emacs_insert_mode, vi_navigation_mode
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.selection import SelectionType

from ...key import Key, ModifierKey
from ..ime import IME


def viemacs(rime: IME) -> None:
    repl = rime.repl

    @repl.add_key_binding("escape", filter=emacs_insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.VI
        event.app.vi_state.input_mode = InputMode.NAVIGATION
        rime.is_enabled = False

    @repl.add_key_binding("i", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        rime.is_enabled = True

    @repl.add_key_binding("a", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        event.current_buffer.cursor_position += (
            event.current_buffer.document.get_cursor_right_position()
        )
        rime.is_enabled = True

    @repl.add_key_binding("I", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        event.current_buffer.cursor_position += (
            event.current_buffer.document.get_start_of_line_position(
                after_whitespace=True
            )
        )
        rime.is_enabled = True

    @repl.add_key_binding("A", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        event.current_buffer.cursor_position += (
            event.current_buffer.document.get_end_of_line_position()
        )
        rime.is_enabled = True

    @repl.add_key_binding("o", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        event.current_buffer.insert_line_below(copy_margin=not in_paste_mode())
        rime.is_enabled = True

    @repl.add_key_binding("O", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        event.current_buffer.insert_line_above(copy_margin=not in_paste_mode())
        rime.is_enabled = True

    @repl.add_key_binding("s", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        text = event.current_buffer.delete(count=event.arg)
        event.app.clipboard.set_text(text)
        rime.is_enabled = True

    @repl.add_key_binding("C", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        buffer = event.current_buffer

        deleted = buffer.delete(
            count=buffer.document.get_end_of_line_position()
        )
        event.app.clipboard.set_text(deleted)
        rime.is_enabled = True

    @repl.add_key_binding("c", "c", filter=vi_navigation_mode)
    @repl.add_key_binding("S", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        buffer = event.current_buffer
        # We copy the whole line.
        data = ClipboardData(buffer.document.current_line, SelectionType.LINES)
        event.app.clipboard.set_data(data)

        # But we delete after the whitespace
        buffer.cursor_position += buffer.document.get_start_of_line_position(
            after_whitespace=True
        )
        buffer.delete(count=buffer.document.get_end_of_line_position())
        rime.is_enabled = True

    @repl.add_key_binding(
        *Key.new("enter", ModifierKey.Shift).keys,
        filter=rime.filter(),
    )
    @repl.add_key_binding(
        *Key.new("enter", ModifierKey.Control).keys,
        filter=rime.filter(),
    )
    @repl.add_key_binding(
        *Key.new("enter", ModifierKey.Control | ModifierKey.Shift).keys,
        filter=rime.filter(),
    )
    @repl.add_key_binding(
        *Key.new("enter", ModifierKey.Shift | ModifierKey.Alt).keys,
        filter=rime.filter(),
    )
    @repl.add_key_binding(
        *Key.new("enter", ModifierKey.Control | ModifierKey.Alt).keys,
        filter=rime.filter(),
    )
    @repl.add_key_binding(
        *Key.new(
            "enter", ModifierKey.Control | ModifierKey.Shift | ModifierKey.Alt
        ).keys,
        filter=rime.filter(),
    )
    def _(event: KeyPressEvent) -> None:
        """`<https://github.com/prompt-toolkit/python-prompt-toolkit/issues/2006>_`

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.current_buffer.validate_and_handle()
