r"""Layout
==========
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text.base import AnyFormattedText
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame
from wcwidth import wcswidth

from .formatted_text import formatted_text


@dataclass
class RimeLayout(Layout):
    r"""Rimelayout."""

    app: Application = field(default_factory=get_app)
    get_input_prompt: Callable[[], AnyFormattedText] = lambda: ""
    content: BufferControl = field(default_factory=BufferControl)

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.window = Window(self.content)
        self.float = Float(Frame(self.window))
        super().__init__(
            FloatContainer(
                self.app.layout.container,
                [self.float],
            )
        )

    def move(self, left: int, top: int) -> None:
        r"""Move.

        :param left:
        :type left: int
        :param top:
        :type top: int
        :rtype: None
        """
        self.float.left = left
        self.float.top = top

    def resize(self, width: int, height: int) -> None:
        r"""Resize.

        :param width:
        :type width: int
        :param height:
        :type height: int
        :rtype: None
        """
        self.window.width = width
        self.window.height = height

    def update(self, lines: tuple[str, ...] = (), col: int = 0) -> None:
        r"""Update.

        :param lines:
        :type lines: tuple[str, ...]
        :param col:
        :type col: int
        :rtype: None
        """
        self.content.buffer.text = "\n".join(lines)
        self.resize(
            (max(wcswidth(line) for line in lines) if len(lines) > 0 else 0),
            len(lines),
        )
        buffer = self.app.layout.current_buffer
        left, top = self.calculate_cursor(buffer) if buffer else (0, 0)
        left += col
        left += wcswidth(formatted_text(self.get_input_prompt()))
        self.move(left, top)

    @staticmethod
    def calculate_cursor(buffer: Buffer) -> tuple[int, int]:
        r"""Calculate the cursor position of a buffer.

        :param buffer:
        :type buffer: Buffer
        :rtype: tuple[int, int]
        """
        lines = buffer.text[: buffer.cursor_position].splitlines()
        top = len(lines)
        left = wcswidth(lines[-1]) if top > 0 else 0
        return left, top
