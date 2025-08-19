"""Insert
=========
"""

from prompt_toolkit.key_binding.key_processor import KeyPressEvent


def insert(event: KeyPressEvent, pre: str, post: str) -> None:
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
