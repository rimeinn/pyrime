r"""Plugins
===========
"""

from .. import IME

try:
    from ..rime import RIME
except ImportError:
    RIME = IME
