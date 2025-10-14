r"""Rime
========
"""

from dataclasses import dataclass, field

from .key import Key, ModifierKey
from .session import Session
from .ui import UI


@dataclass
class RimeBase:
    session: Session = field(default_factory=Session)
    ui: UI = field(default_factory=UI)

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

    def __call__(self, *keys: Key):
        r"""Call.

        :param self:
        :param keys: Key
        :type keys: str
        """
        text, lines, _ = self.draw(*keys)
        print(text)
        print("\n".join(lines))
