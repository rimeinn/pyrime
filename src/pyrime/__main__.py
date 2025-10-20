r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

from getch import getch

from .key import BasicKey, Key
from .rime import RimeBase

if __name__ == "__main__":
    rime = RimeBase()
    rime.is_enabled = True
    while True:
        try:
            c = getch()
        except OverflowError:
            break
        key = Key(BasicKey(ord(c)))
        rime(print, key)
