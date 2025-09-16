r"""Rime for Ptpython
=====================

``RIME`` inherits ``pyrime.ptpython``'s ``IME`` to use ``Session``s OOP APIs to
call librime on the basis of ``IME``.
"""

from dataclasses import dataclass

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    Window,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame
from wcwidth import wcswidth

from ..api import Traits
from ..key import Key, ModifierKey
from ..session import Session
from ..ui import UI
from . import IME


@dataclass
class RIME(IME):
    r"""RIME inherit IME."""

    remember_rime: bool = False
    window: Window = None  # type: ignore
    layout: Layout | None = None
    traits: Traits | None = None
    ui: UI = None  # type: ignore
    keys_set: set[tuple[str, ...]] = None  # type: ignore

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.session = Session(self.traits)
        self.traits = self.session.traits
        if self.ui is None:
            self.ui = UI()
        if self.keys_set is None:
            self.keys_set = {
                ("s-tab",),
                ("s-escape",),
                ("escape", "backspace"),
                ("escape", "enter"),
                Key.new("enter", ModifierKey.Shift).keys,
                Key.new("enter", ModifierKey.Control).keys,
                Key.new("enter", ModifierKey.Shift | ModifierKey.Control).keys,
                Key.new("enter", ModifierKey.Shift | ModifierKey.Alt).keys,
                Key.new("enter", ModifierKey.Control | ModifierKey.Alt).keys,
                Key.new(
                    "enter",
                    ModifierKey.Shift | ModifierKey.Control | ModifierKey.Alt,
                ).keys,
            }
            for order in range(ord(" "), ord("~") + 1):
                self.keys_set |= {(chr(order),)}
            for number in range(1, 24):
                self.keys_set |= {(f"f{number}",)}
            for keyname in {
                "insert",
                "delete",
                "up",
                "down",
                "left",
                "right",
                "home",
                "end",
                "pageup",
                "pagedown",
            }:
                self.keys_set |= {
                    (keyname,),
                    ("c-" + keyname,),
                    ("s-" + keyname,),
                    ("c-s-" + keyname,),
                    ("escape", keyname),
                    ("escape", "c-" + keyname),
                    ("escape", "s-" + keyname),
                    ("escape", "c-s-" + keyname),
                }
            for order in range(ord("@"), ord("[")):
                key = "c-" + chr(order).lower()
                self.keys_set |= {(key,), ("escape", key)}
            self.keys_set |= {("escape", "escape")}
            for order in range(ord("[") + 1, ord("_")):
                key = "c-" + chr(order)
                self.keys_set |= {(key,), ("escape", key)}
            for order in range(ord(" "), ord("~") + 1):
                self.keys_set |= {("escape", chr(order))}

        for keys in self.keys_set:
            keys = list(keys)

            @self.repl.add_key_binding(*keys, filter=self.mode(keys))  # type: ignore
            def _(event: KeyPressEvent, keys: list[str] = keys) -> None:
                r""".

                :param event:
                :type event: KeyPressEvent
                :param keys:
                :type keys: list[str]
                :rtype: None
                """
                self.key_binding(event, keys)

    def mode(self, keys: list[str]) -> Condition:
        r"""Mode.

        :param keys:
        :type keys: list[str]
        :rtype: Condition
        """

        @Condition
        def _(keys: list[str] = keys) -> bool:
            r""".

            :param keys:
            :type keys: list[str]
            :rtype: bool
            """
            if len(keys) == 1 == len(keys[0]):
                return self.is_enabled
            if len(keys) == 1 or len(keys) > 1 and keys[0] == "escape":
                return self.preedit != ""
            raise NotImplementedError

        return _

    def key_binding(self, event: KeyPressEvent, keys: list[str]) -> None:
        r"""Key binding.

        :param event:
        :type event: KeyPressEvent
        :param keys:
        :type keys: list[str]
        :rtype: None
        """
        text, lines, col = self.draw(keys)
        self.preedit = lines[0].strip(" " + self.ui.cursor)
        ui_text = "\n".join(lines)
        event.cli.current_buffer.insert_text(text)
        self.window.height = len(lines)
        if len(lines):
            self.window.width = max(wcswidth(line) for line in lines)
        self.window.content.buffer.text = ui_text  # type: ignore
        left, top = self.calculate()
        left += col
        self.repl.app.layout.container.floats[0].left = left  # type: ignore
        self.repl.app.layout.container.floats[0].top = top  # type: ignore

    def draw(self, keys: list[str]) -> tuple[str, list[str], int]:
        r"""Draw.

        :param keys:
        :type keys: list[str]
        :rtype: tuple[str, list[str], int]
        """
        key = Key.new(keys)
        if not self.session.process_key(key.code, key.mask):
            if len(keys) == 1 == len(keys[0]):
                return keys[0], [self.ui.cursor], 0
            return "", [self.ui.cursor], 0
        context = self.session.get_context()
        if context is None or context.menu.num_candidates == 0:
            return self.session.get_commit_text(), [self.ui.cursor], 0
        lines, col = self.ui.draw(context)
        return "", lines, col

    def swap_layout(self):
        r"""Swap layout."""
        (self.layout, self.repl.app.layout) = (  # type: ignore
            self.repl.app.layout,
            self.layout,
        )

    def disable(self) -> None:
        r"""Disable.

        :rtype: None
        """
        self.swap_layout()
        self.is_enabled = False
        self.preedit = ""
        self.session.clear_composition()

    def calculate(self) -> tuple[int, int]:
        r"""Calculate.

        :rtype: tuple[int, int]
        """
        left = 0
        for _, text in self.repl.all_prompt_styles[  # type: ignore
            self.repl.prompt_style
        ].in_prompt():
            left += wcswidth(text)
        top = 0
        if self.repl.app.layout.current_buffer:
            lines = self.repl.app.layout.current_buffer.text[
                : self.repl.app.layout.current_buffer.cursor_position
            ].split("\n")
            top += len(lines)
            left += wcswidth(lines[-1])
        return left, top

    def enable(self) -> None:
        r"""Enable.

        :rtype: None
        """
        left, top = self.calculate()
        self.window = Window(
            BufferControl(buffer=Buffer()),
            width=wcswidth(self.ui.cursor),
            height=1,
        )
        self.window.content.buffer.text = self.ui.cursor  # type: ignore
        self.layout = Layout(
            FloatContainer(  # type: ignore
                self.repl.app.layout.container,
                [
                    Float(
                        Frame(
                            self.window,
                        ),
                        left=left,
                        top=top,
                    )
                ],
            )
        )
        self.swap_layout()
        self.is_enabled = True

    def conditional_disable(self) -> None:
        r"""Conditional disable.

        :rtype: None
        """
        if self.is_enabled:
            self.remember_rime = True
            self.disable()

    def conditional_enable(self) -> None:
        r"""Conditional enable.

        :rtype: None
        """
        if self.remember_rime:
            self.enable()

    def toggle(self) -> None:
        r"""Toggle.

        :rtype: None
        """
        if self.is_enabled:
            self.disable()
        else:
            self.enable()
