r"""Vertical
============

Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/ui/vertical.lua>
"""

from dataclasses import dataclass

from .. import Context
from . import STYLES, UI


@dataclass
class VerticalUI(UI):
    r"""Vertical UI."""

    indices: tuple[str, ...] = STYLES["circle"]
    left_sep: str = "["
    right_sep: str = "]"
    cursor: str = "|"

    def draw(self, context: Context) -> tuple[tuple[str, ...], int]:
        r"""Draw UI.

        :param self:
        :param context:
        :type context: Context
        :rtype: tuple[tuple[str, ...], int]
        """
        if context.composition.preedit is None:
            preedit = ""
        else:
            preedit = context.composition.preedit
        preedit = (
            preedit[0 : context.composition.cursor_pos]
            + self.cursor
            + preedit[context.composition.cursor_pos :]
        )

        lines = (preedit,)
        candidates = context.menu.candidates
        indices = self.indices
        for index, candidate in enumerate(candidates):
            text = indices[index] + " " + candidate.text
            if candidate.comment:
                text = text + " " + candidate.comment
            if context.menu.highlighted_candidate_index == index:
                text = self.left_sep + text + self.right_sep
            else:
                text = " " + text + " "
            lines += (text,)

        return lines, 0
