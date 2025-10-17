r"""IME
=======

``RimeBase`` only accept input and output to stdout. An effective IME can be
toggle. So we wrap a ``IMEBase`` for ptpython, pynvim and ...
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class IMEBase:
    r"""Base for ``IME``.

    Any subclass should define ``exe()`` and ``switch()``.
    """

    def __post_init__(self) -> None:
        self.is_enabled = False

    def exe(self, *args: Any, **kwargs: Any) -> None:
        r"""Execute.

        :param args:
        :type args: Any
        :param kwargs:
        :type kwargs: Any
        :rtype: None
        """
        print(args, kwargs)

    def switch(self) -> None:
        r"""Switch IME to ``self.is_enabled``.

        :rtype: None
        """
        print(self.is_enabled)

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

    def toggle(self, is_enabled: bool | None = None) -> None:
        r"""Toggle IME only if required. Wrap ``self.switch()``.

        :param is_enabled:
        :type is_enabled: bool | None
        :rtype: None
        """
        if is_enabled is None:
            is_enabled = not self.is_enabled
        if self.is_enabled is is_enabled:
            return
        self.is_enabled = is_enabled
        self.switch()

    def enable(self) -> None:
        r"""Enable. Wrap ``self.toggle()``.

        :rtype: None
        """
        self.toggle(True)

    def disable(self) -> None:
        r"""Disable. Wrap ``self.toggle()``.

        :rtype: None
        """
        self.toggle(False)
