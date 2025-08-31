r"""Plugins
===========

In some python environments such as ``gdb``, 3rd binary python module cannot be
imported. Use ``IME`` to replace ``RIME``.
"""

from .. import IME

try:
    from ..rime import RIME
except ImportError:
    RIME = IME
