r"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

from dataclasses import dataclass
from enum import Enum, auto

__version__ = "@PROJECT_VERSION@"
# wrong rime.distribution_version will result in error
if "@" in __version__:
    __version__ = "0.0.1"


class LogLevel(Enum):
    INFO = 0
    WARNING = auto()
    ERROR = auto()
    FATAL = auto()


@dataclass
class SchemaListItem:
    r"""Schemalistitem."""

    schema_id: str
    name: str


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
class SessionBase:
    r"""A session for Rime"""

    def __post_init__(self):
        r"""Post init.

        :param self:
        """

    def __del__(self) -> None:
        r"""Del.

        :param self:
        :rtype: None
        """

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
