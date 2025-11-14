r"""Nvim
========

This directory display how to use rime to create a neovim plugin.
NOTE: it is only for demonstration. A real plugin which can be used in product
environment is <https://github.com/rimeinn/rime.nvim>.
"""

import os
from glob import glob

import pynvim
from pynvim.api.nvim import Nvim


def get_default_nvim() -> Nvim:
    r"""Get default nvim.

    :rtype: Nvim
    """
    paths = glob(f"/run/user/{os.getuid()}/nvim.*")
    if len(paths) > 0:
        return pynvim.attach("socket", path=paths[-1])
    return pynvim.attach(
        "child", argv=["/usr/bin/env", "nvim", "--embed", "--headless"]
    )
