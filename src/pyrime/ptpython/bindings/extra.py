r"""Extra
=========
"""

from typing import TYPE_CHECKING

from prompt_toolkit.filters.app import emacs_insert_mode, vi_navigation_mode
from prompt_toolkit.key_binding.bindings.named_commands import (
    backward_char,
    forward_char,
    unix_word_rubout,
)
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys

from .rime import EXTRA_KEYS_SET

if TYPE_CHECKING:
    from ..ime import IME


def load_extra_bindings(rime: "IME") -> KeyBindings:
    r"""Extra.

    :param rime:
    :type rime: IME
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    for keys in EXTRA_KEYS_SET:

        @handle(*keys, filter=~rime.preedit_available)
        def _(event: KeyPressEvent) -> None:
            """`<https://github.com/prompt-toolkit/python-prompt-toolkit/issues/2006>_`

            :param event:
            :type event: KeyPressEvent
            :rtype: None
            """
            event.current_buffer.validate_and_handle()

    @handle(Keys.ControlJ, filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        buffer = event.current_buffer
        buffer.newline()

    @handle(
        Keys.ControlX,
        Keys.ControlJ,
        filter=emacs_insert_mode & ~rime.preedit_available,
    )
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        buffer = event.current_buffer
        buffer.join_next_line()

    @handle(Keys.Escape, "m", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        b = event.cli.current_buffer
        c: int = 0
        while b.document.char_before_cursor == " ":
            backward_char(event)
            c += 1
        w: str = b.document.get_word_before_cursor()
        for _ in range(c):
            forward_char(event)
        event.cli.current_buffer.insert_text(w)

    @handle(Keys.Escape, "w", filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        unix_word_rubout(event)

    @handle(Keys.ControlX, Keys.ControlE, filter=insert_mode)
    @handle("g", "h", filter=vi_navigation_mode & ~rime.preedit_available)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        buffer = event.current_buffer
        buffer.open_in_editor()

    @handle(Keys.ControlBackslash, filter=insert_mode)
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        buffer = event.current_buffer
        buffer.cancel_completion()

    return key_bindings
