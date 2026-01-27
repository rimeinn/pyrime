r"""Horizontal
==============

Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/ui/horizontal.lua>
"""

from dataclasses import dataclass

from wcwidth import wcswidth

from .. import Context
from . import STYLES, UI


@dataclass
class HorizontalUI(UI):
    r"""Horizontal UI."""

    indices: tuple[str, ...] = STYLES["circle"]
    left: str = "<|"
    right: str = "|>"
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

        candidates = context.menu.candidates
        line = ""
        indices = self.indices
        for index, candidate in enumerate(candidates):
            text = indices[index] + " " + candidate.text
            if candidate.comment:
                text = text + " " + candidate.comment
            if context.menu.highlighted_candidate_index == index:
                text = self.left_sep + text
            elif context.menu.highlighted_candidate_index + 1 == index:
                text = self.right_sep + text
            else:
                text = " " + text
            line = line + text
        if (
            context.menu.num_candidates
            == context.menu.highlighted_candidate_index + 1
        ):
            line = line + self.right_sep
        else:
            line = line + " "
        col = 0
        left = self.left
        if context.menu.page_no != 0:
            num = wcswidth(self.left)
            line = left + line
            preedit = " " * num + preedit
            col = col - num
        if not context.menu.is_last_page and context.menu.num_candidates > 0:
            line = line + self.right

        return (preedit, line), col
