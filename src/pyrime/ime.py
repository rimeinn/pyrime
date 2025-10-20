r"""IME
=======

``RimeBase`` only accept input and output to stdout. An effective IME can be
toggled. So we wrap a ``IMEBase`` for ptpython, pynvim and ...
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class IMEBase:
    r"""Base for ``IME``.

    Any subclass should define ``exe()``.
    """

    @property
    def is_enabled(self) -> bool:
        return True

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        pass

    def exe(self, *args: Any, **kwargs: Any) -> None:
        r"""Execute.

        :param args:
        :type args: Any
        :param kwargs:
        :type kwargs: Any
        :rtype: None
        """
        print(args, kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        r"""Call ``self.exe()`` only if required.

        :param args:
        :type args: Any
        :param kwargs:
        :type kwargs: Any
        :rtype: None
        """
        if self.is_enabled:
            self.exe(*args, **kwargs)
