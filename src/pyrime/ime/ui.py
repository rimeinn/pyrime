r"""Draw UI
===========

Draw UI of IME.
Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/ui.lua>
"""

from dataclasses import dataclass

from wcwidth import wcswidth

from . import Context

# https://github.com/Freed-Wu/tmux-digit/blob/547226faa6ea32b3805bcd9a5a54bf943b8e4c48/digit.tmux#L3-L9
STYLES = {
    "circle": ("①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⓪"),
    "circle_inv": ("󰲠", "󰲢", "󰲤", "󰲦", "󰲨", "󰲪", "󰲬", "󰲮", "󰲰", "0"),
    "square": ("󰎦", "󰎩", "󰎬", "󰎮", "󰎰", "󰎵", "󰎸", "󰎻", "󰎾", "󰎣"),
    "square_inv": ("󰎤", "󰎧", "󰎪", "󰎭", "󰎱", "󰎳", "󰎶", "󰎹", "󰎼", "󰎡"),
    "layer": ("󰎥", "󰎨", "󰎫", "󰎲", "󰎯", "󰎴", "󰎷", "󰎺", "󰎽", "󰎢"),
    "layer_inv": ("󰼏", "󰼐", "󰼑", "󰼒", "󰼓", "󰼔", "󰼕", "󰼖", "󰼗", "󰼎"),
    "number": ("󰬺", "󰬻", "󰬼", "󰬽", "󰬾", "󰬿", "󰭀", "󰭁", "󰭂", ""),
}


@dataclass
class UI:
    r"""UI."""

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
        candidates_ = ""
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
            candidates_ = candidates_ + text
        if (
            context.menu.num_candidates
            == context.menu.highlighted_candidate_index + 1
        ):
            candidates_ = candidates_ + self.right_sep
        else:
            candidates_ = candidates_ + " "
        col = 0
        left = self.left
        if context.menu.page_no != 0:
            num = wcswidth(self.left)
            candidates_ = left + candidates_
            preedit = " " * num + preedit
            col = col - num
        if not context.menu.is_last_page and context.menu.num_candidates > 0:
            candidates_ = candidates_ + self.right
        return (preedit, candidates_), col
