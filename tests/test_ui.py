r"""Test draw UI."""

from pyrime.ime import Candidate, Composition, Context, Menu
from pyrime.ime.ui import UI


class Test:
    r"""Test."""

    @staticmethod
    def test_ui() -> None:
        r"""Test draw UI.

        :rtype: None
        """
        context = Context(
            composition=Composition(
                length=1,
                cursor_pos=1,
                sel_start=0,
                sel_end=1,
                preedit="w",
            ),
            menu=Menu(
                page_size=10,
                page_no=0,
                is_last_page=False,
                highlighted_candidate_index=0,
                num_candidates=10,
                select_keys=None,
                candidates=[
                    Candidate(text="我", comment=None),
                    Candidate(text="为", comment=None),
                    Candidate(text="玩", comment=None),
                    Candidate(text="问", comment=None),
                    Candidate(text="无", comment=None),
                    Candidate(text="万", comment=None),
                    Candidate(text="完", comment=None),
                    Candidate(text="网", comment=None),
                    Candidate(text="王", comment=None),
                    Candidate(text="外", comment=None),
                ],
            ),
        )
        ui = UI()
        lines = ("w|", "[① 我]② 为 ③ 玩 ④ 问 ⑤ 无 ⑥ 万 ⑦ 完 ⑧ 网 ⑨ 王 ⓪ 外 |>")
        assert ui.draw(context) == (lines, 0)
