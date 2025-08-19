r"""Draw UI
===========

A function to draw UI of IME.
"""

from dataclasses import dataclass

from wcwidth import wcswidth

from . import Context


@dataclass
class UI:
    r"""UI."""

    indices: list[str] = None  # type: ignore
    left: str = "<|"
    right: str = "|>"
    left_sep: str = "["
    right_sep: str = "]"
    cursor: str = "|"

    def __post_init__(self) -> None:
        if self.indices is None:
            self.indices = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⓪"]


def draw_ui(context: Context, ui: UI) -> tuple[list[str], int]:
    r"""Draw UI.

    :param context:
    :type context: Context
    :param ui:
    :type ui: UI
    :rtype: tuple[list[str], int]
    """
    if context.composition.preedit is None:
        preedit = ""
    else:
        preedit = context.composition.preedit
    preedit = (
        preedit[0 : context.composition.cursor_pos]
        + ui.cursor
        + preedit[context.composition.cursor_pos :]
    )
    candidates = context.menu.candidates
    candidates_ = ""
    indices = ui.indices
    for index, candidate in enumerate(candidates):
        text = indices[index] + " " + candidate.text
        if candidate.comment:
            text = text + " " + candidate.comment
        if context.menu.highlighted_candidate_index == index:
            text = ui.left_sep + text
        elif context.menu.highlighted_candidate_index + 1 == index:
            text = ui.right_sep + text
        else:
            text = " " + text
        candidates_ = candidates_ + text
    if (
        context.menu.num_candidates
        == context.menu.highlighted_candidate_index + 1
    ):
        candidates_ = candidates_ + ui.right_sep
    else:
        candidates_ = candidates_ + " "
    col = 0
    left = ui.left
    if context.menu.page_no != 0:
        num = wcswidth(ui.left)
        candidates_ = left + candidates_
        preedit = " " * num + preedit
        col = col - num
    if not context.menu.is_last_page and context.menu.num_candidates > 0:
        candidates_ = candidates_ + ui.right
    return [preedit, candidates_], col
