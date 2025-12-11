r"""Rime
========

Refer <https://github.com/rimeinn/rime.nvim/blob/main/lua/rime/rime.lua>
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass, field

from .ime.ime import IMEBase
from .ime.ui import UI
from .key import Key
from .utils import SessionBase

logger = logging.getLogger(__name__)


def get_session() -> SessionBase:
    r"""Get a session.

    In some python environments such as ``gdb``, 3rd binary python module
    cannot be imported. Use ``IME`` to replace ``RIME``.
    """
    try:
        from .session import Session as cls
    except ImportError as e:
        logger.warning(e.msg)
        cls = SessionBase
    return cls()


@dataclass
class RimeBase(IMEBase):
    r"""Base for ``Rime``.

    Provides ``draw()``.
    """

    session: SessionBase = field(default_factory=get_session)
    ui: UI = field(default_factory=UI)
    enabled: bool = False

    def draw(self, *keys: Key) -> tuple[str, tuple[str, ...], int]:
        r"""Wrap ``UI.draw()``.

        :param keys:
        :type keys: Key
        :rtype: tuple[str, tuple[str, ...], int]
        """
        for key in keys:
            if not self.session.process_key(*key):
                return str(key), (), 0
        context = self.session.get_context()
        if context is None or context.menu.num_candidates == 0:
            return self.session.get_commit_text(), (), 0
        lines, col = self.ui.draw(context)
        return "", lines, col

    def exe(self, callback: Callable[[str], None], *keys: Key) -> None:
        r"""Override ``IMEBase``.

        :param self:
        :param callback:
        :type callback: Callable[[str], None]
        :param keys:
        :type keys: Key
        :rtype: None
        """
        text, lines, _ = self.draw(*keys)
        callback(text)
        print("\n".join(lines))

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        if not enabled:
            self.session.clear_composition()
        self.enabled = enabled
