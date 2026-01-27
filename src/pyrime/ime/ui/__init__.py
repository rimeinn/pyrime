r"""Draw UI
===========

Draw UI of IME.
Refer <https://github.com/rimeinn/ime.nvim/blob/0.0.5/packages/ime/lua/ime/ui.lua>
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .. import Context

# https://github.com/Freed-Wu/tmux-digit/blob/547226faa6ea32b3805bcd9a5a54bf943b8e4c48/digit.tmux#L3-L9
STYLES = {
    "circle": ("①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⓪"),
    "circle_inv": ("󰲠", "󰲢", "󰲤", "󰲦", "󰲨", "󰲪", "󰲬", "󰲮", "󰲰", "0"),
    "square": ("󰎦", "󰎩", "󰎬", "󰎮", "󰎰", "󰎵", "󰎸", "󰎻", "󰎾", "󰎣"),
    "square_inv": ("󰎤", "󰎧", "󰎪", "󰎭", "󰎱", "󰎳", "󰎶", "󰎹", "󰎼", "󰎡"),
    "layer": ("󰎥", "󰎨", "󰎫", "󰎲", "󰎯", "󰎴", "󰎷", "󰎺", "󰎽", "󰎢"),
    "layer_inv": ("󰼏", "󰼐", "󰼑", "󰼒", "󰼓", "󰼔", "󰼕", "󰼖", "󰼗", "󰼎"),
    "number": ("󰬺", "󰬻", "󰬼", "󰬽", "󰬾", "󰬿", "󰭀", "󰭁", "󰭂", ""),
}


@dataclass
class UI(ABC):
    r"""UI."""

    @abstractmethod
    def draw(self, context: Context) -> tuple[tuple[str, ...], int]:
        r"""Draw UI.

        :param self:
        :param context:
        :type context: Context
        :rtype: tuple[tuple[str, ...], int]
        """
