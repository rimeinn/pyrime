r"""Plugins
===========
"""

from .. import RimeBase

try:
    from ..rime import Rime
except ImportError:
    Rime = RimeBase
