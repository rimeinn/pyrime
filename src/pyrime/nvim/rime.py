r"""Rime for Neovim
===================

Refer <https://github.com/rimeinn/rime.nvim/blob/main/lua/rime/nvim/rime.lua>

TODO: cannot get ``v:char`` in pynvim. we must refer
<http://github.com/rimeinn/coc-rime> to pass input character directly, which is
troublesome. That is why this plugin is experimental and not recommended to use
in product environment just as coc-rime.
"""

from dataclasses import dataclass, field

import pynvim
from pynvim.api.nvim import Nvim

from ..rime import RimeBase
from . import get_default_nvim
from .keymap import Keymap
from .win import Win


@pynvim.plugin
@dataclass
class Rime(RimeBase):
    r"""Rime for neovim.

    Provide:
        vim function ``rime_set(v:true/v:false/v:null)``.
        vim command ``:Rime enable/disable/toggle``.
    """

    vim: Nvim = field(default_factory=get_default_nvim)
    nowait: tuple[str, ...] = Keymap.nowait
    special: tuple[str, ...] = Keymap.special
    disable: tuple[str, ...] = Keymap.disable
    augroup_name: str = "rime"

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.win = Win(self.vim.api)
        self.keymap = Keymap(
            self.vim.api, self.nowait, self.special, self.disable
        )
        self.augroup_id = self.vim.api.create_augroup(self.augroup_name, {})
        self.create_autocmds(self.augroup_id)

    def create_autocmds(self, id: int):
        r"""Create autocmds.

        TODO

        :param id:
        :type id: int
        """

    def exe(self, input: str) -> None:  # type: ignore
        r"""Exe.

        TODO

        :param input:
        :type input: str
        :rtype: None
        """

    @pynvim.function("rime_set")
    def function(self, flag: bool | None) -> None:
        r"""Function.

        :param flag:
        :type flag: bool | None
        :rtype: None
        """
        if flag is None:
            flag = not self.is_enabled
        self.is_enabled = flag

    @pynvim.command("Rime")
    def command(self, args: list[str]) -> None:
        r"""Command.

        :param args:
        :type args: list[str]
        :rtype: None
        """
        if args and args[0] == "enable":
            self.is_enabled = True
        elif args and args[0] == "disable":
            self.is_enabled = False
        else:
            self.is_enabled = not self.is_enabled

    @property
    def is_enabled(self) -> bool:
        r"""Is enabled.

        :rtype: bool
        """
        return self.vim.current.buffer.vars.get("iminsert", False)

    @is_enabled.setter
    def is_enabled(self, enabled: bool) -> None:
        r"""Is enabled.

        :param enabled:
        :type enabled: bool
        :rtype: None
        """
        if self.vim.current.buffer.vars.get("iminsert", False) != enabled:
            self.vim.current.buffer.vars["iminsert"] = enabled
            self.keymap.set_nowait(enabled)
