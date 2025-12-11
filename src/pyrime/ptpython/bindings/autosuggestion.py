r"""Autosuggestion
==================

Refer `zsh-autosuggestions <https://github.com/zsh-users/zsh-autosuggestions>`_.
"""

import re
from typing import TYPE_CHECKING

from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys

if TYPE_CHECKING:
    from ..ime import IME


def load_autosuggestion_bindings(rime: "IME") -> KeyBindings:
    r"""Autosuggestion.

    :param rime:
    :type rime: IME
    :rtype: KeyBindings
    """
    key_bindings = KeyBindings()
    insert_mode = rime.insert_mode
    handle = key_bindings.add

    @Condition
    def suggestion_available() -> bool:
        """Suggestion available.

        :rtype: bool
        """
        app = rime.app
        return (
            app.current_buffer.suggestion is not None
            and len(app.current_buffer.suggestion.text) > 0
            and app.current_buffer.document.is_cursor_at_the_end
        )

    @handle(Keys.Right, filter=suggestion_available & insert_mode)
    @handle(Keys.ControlF, filter=suggestion_available & insert_mode)
    def _(event: "KeyPressEvent") -> None:
        """.

        :param event:
        :type event: "KeyPressEvent"
        :rtype: None
        """
        b = event.current_buffer
        suggestion = b.suggestion

        if suggestion and event.arg > 0:
            b.insert_text(
                suggestion.text[0 : min(event.arg, len(suggestion.text))]
            )

    @handle(
        Keys.ControlSquareClose,
        Keys.Any,
        filter=suggestion_available & insert_mode,
    )
    def _(event: "KeyPressEvent") -> None:
        """.

        :param event:
        :type event: "KeyPressEvent"
        :rtype: None
        """
        b = event.current_buffer
        suggestion = b.suggestion

        # don't support event.arg
        if suggestion and event.arg > 0:
            t = re.split(event.data, suggestion.text)
            b.insert_text(next(x for x in t if x))
            if len(t) != 1:
                b.insert_text(event.data)

    return key_bindings
