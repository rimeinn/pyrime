r"""Ptpython
============

In some python environments such as ``gdb``, 3rd binary python module cannot be
imported. Use ``IME`` to replace ``RIME``.
"""

try:
    from .rime import Rime as RIME
except ImportError:
    from .ime import IME as RIME  # noqa: F401
