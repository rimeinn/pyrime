r"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

import os, sys
from dataclasses import dataclass
from enum import Enum, auto

__version__ = "@PROJECT_VERSION@"
# wrong rime.distribution_version will result in error
if "@" in __version__:
    __version__ = "0.0.1"

if sys.platform == "win32":
    lib_dir = os.environ.get("LIBRIME_LIB_DIR")
    if lib_dir and os.path.isdir(lib_dir):
        os.add_dll_directory(lib_dir)


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
