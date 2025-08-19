r"""Autosuggestion
==================

Refer `zsh-autosuggestions <https://github.com/zsh-users/zsh-autosuggestions>`_.
"""

import re

from prompt_toolkit.filters import (
    Condition,
    ViInsertMode,
    emacs_mode,
)
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from ptpython.repl import PythonRepl


def autosuggestion(repl: PythonRepl) -> None:
    r"""Autosuggestion.

    :param repl:
    :type repl: PythonRepl
    :rtype: None
    """

    @Condition
    def suggestion_available() -> bool:
        """Suggestion available.

        :rtype: bool
        """
        app = repl.app
        return (
            app.current_buffer.suggestion is not None
            and len(app.current_buffer.suggestion.text) > 0
            and app.current_buffer.document.is_cursor_at_the_end
        )

    @repl.add_key_binding(
        "right",
        filter=suggestion_available & ViInsertMode(),  # type: ignore
    )
    @repl.add_key_binding("right", filter=suggestion_available & emacs_mode)  # type: ignore
    @repl.add_key_binding("c-f", filter=suggestion_available & ViInsertMode())  # type: ignore
    @repl.add_key_binding("c-f", filter=suggestion_available & emacs_mode)  # type: ignore
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

    @repl.add_key_binding(
        "c-]",
        Keys.Any,  # type: ignore
        filter=suggestion_available & emacs_mode,  # type: ignore
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
