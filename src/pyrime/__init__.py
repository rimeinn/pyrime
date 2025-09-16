r"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

from dataclasses import dataclass
from enum import Enum, auto

__version__ = "@PROJECT_VERSION@"


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
