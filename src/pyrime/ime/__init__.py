r"""pyime
=========

A library related to input method engine for ptpython/neovim like
<https://github.com/rimeinn/rime.nvim/tree/0.2.12/packages/ime>

Currently, only one IME pyrime use this library.
If any other IME such as pyfcitx is realized, this library can be standalone
like <https://luarocks.org/modules/freed-wu/ime> named pyime.
"""

from dataclasses import dataclass


@dataclass
class Composition:
    r"""Composition."""

    length: int
    cursor_pos: int
    sel_start: int
    sel_end: int
    preedit: str | None


@dataclass
class Candidate:
    r"""Candidate."""

    text: str
    comment: str | None


@dataclass
class Menu:
    r"""Menu."""

    page_size: int
    page_no: int
    is_last_page: bool
    highlighted_candidate_index: int
    num_candidates: int
    select_keys: str | None
    candidates: list[Candidate]


@dataclass
class Context:
    r"""Context."""

    composition: Composition
    menu: Menu


@dataclass
class Commit:
    r"""Commit."""

    text: str
