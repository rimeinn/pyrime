r"""Win
=======

Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/nvim/win.lua>
"""

from dataclasses import dataclass, field
from typing import Any

from pynvim.api.common import RemoteApi
from wcwidth import wcswidth


@dataclass
class Win:
    r"""Win."""

    api: RemoteApi
    win_id: int = -1
    lines: tuple[str, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.buf_id = self.api.create_buf(False, True)

    @property
    def is_valid(self) -> bool:
        r"""Is valid.

        :rtype: bool
        """
        return self.api.win_is_valid(self.win_id)

    @property
    def has_preedit(self) -> bool:
        r"""Has preedit.

        :rtype: bool
        """
        return len(self.lines) == 2

    def update(self, lines: tuple[str, ...] = (), col: int = 0) -> None:
        r"""Update.

        :param lines:
        :type lines: tuple[str, ...]
        :param col:
        :type col: int
        :rtype: None
        """
        self.lines = lines
        width = max(wcswidth(line) for line in lines)
        self.config = {
            "relative": "cursor",
            "height": len(self.lines),
            "style": "minimal",
            "width": width,
            "row": 1,
            "col": col,
        }
        if len(self.lines) == 0:
            if self.is_valid:
                self.api.win_close(self.win_id, False)
            return
        self.api.buf_set_lines(
            self.buf_id, 0, len(self.lines), False, self.lines
        )
        if self.is_valid:
            self.api.win_set_config(self.win_id, self.config)
        else:
            self.win_id = self.api.open_win(self.buf_id, False, self.config)
