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
    r"""Schema list item."""

    schema_id: str
    name: str
