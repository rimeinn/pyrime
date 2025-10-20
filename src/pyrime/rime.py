r"""Rime
========
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from .ime import IMEBase
from .key import Key, ModifierKey
from .session import Session
from .ui import UI


@dataclass
class RimeBase(IMEBase):
    r"""Base for ``Rime``.

    Provides ``draw()``.
    """

    session: Session = field(default_factory=Session)
    ui: UI = field(default_factory=UI)
    enabled: bool = False

    def draw(self, *keys: Key) -> tuple[str, list[str], int]:
        r"""Wrap ``UI.draw()``.

        :param keys:
        :type keys: Key
        :rtype: tuple[str, list[str], int]
        """
        for key in keys:
            if not self.session.process_key(key.code, key.mask):
                return (
                    key.basic.pt_name
                    if key.basic.pt_name != "space"
                    else " "
                    if key.modifier == ModifierKey.NULL
                    else "",
                    [self.ui.cursor],
                    0,
                )
        context = self.session.get_context()
        if context is None or context.menu.num_candidates == 0:
            return self.session.get_commit_text(), [self.ui.cursor], 0
        lines, col = self.ui.draw(context)
        return "", lines, col

    def exe(self, callback: Callable[[str], None], *keys: Key) -> None:
        r"""Override ``IMEBase``.

        :param self:
        :param callback:
        :type callback: Callable[[str], None]
        :param keys:
        :type keys: Key
        :rtype: None
        """
        text, lines, _ = self.draw(*keys)
        callback(text)
        print("\n".join(lines))

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        if not enabled:
            self.session.clear_composition()
        self.enabled = enabled
