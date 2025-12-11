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


@dataclass
class SchemaListItem:
    r"""Schema list item."""

    schema_id: str
    name: str


@dataclass
class SessionBase:
    r"""A dummy session."""

    def process_key(self, keycode: int, mask: int) -> bool:
        r"""Process key.

        :param self:
        :param keycode:
        :type keycode: int
        :param mask:
        :type mask: int
        :rtype: bool
        """
        return False

    def get_context(self) -> Context | None:
        r"""Get context.

        :param self:
        :rtype: Context | None
        """
        return None

    def get_commit(self) -> Commit | None:
        r"""Get commit.

        :param self:
        :rtype: Commit | None
        """
        return None

    def get_current_schema(self) -> str:
        r"""Get current schema.

        :param self:
        :rtype: str
        """
        return ""

    def get_schema_list(self) -> list[SchemaListItem]:
        r"""Get schema list.

        :param self:
        :rtype: list[SchemaListItem]
        """
        return []

    def select_schema(self, schema_id: str) -> bool:
        r"""Select schema.

        :param self:
        :param schema_id:
        :type schema_id: str
        :rtype: bool
        """
        return False

    def commit_composition(self) -> bool:
        r"""Commit composition.

        :param self:
        :rtype: bool
        """
        return False

    def clear_composition(self) -> None:
        r"""Clear composition.

        :param self:
        :rtype: None
        """

    def get_commit_text(self) -> str:
        r"""Get commit text.

        :param self:
        :rtype: str
        """
        return ""
