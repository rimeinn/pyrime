# pyrime

[![readthedocs](https://shields.io/readthedocs/pyrime)](https://pyrime.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/rimeinn/pyrime/main.svg)](https://results.pre-commit.ci/latest/github/rimeinn/pyrime/main)
[![github/workflow](https://github.com/rimeinn/pyrime/actions/workflows/main.yml/badge.svg)](https://github.com/rimeinn/pyrime/actions)
[![codecov](https://codecov.io/gh/rimeinn/pyrime/branch/main/graph/badge.svg)](https://codecov.io/gh/rimeinn/pyrime)

[![github/downloads](https://shields.io/github/downloads/rimeinn/pyrime/total)](https://github.com/rimeinn/pyrime/releases)
[![github/downloads/latest](https://shields.io/github/downloads/rimeinn/pyrime/latest/total)](https://github.com/rimeinn/pyrime/releases/latest)
[![github/issues](https://shields.io/github/issues/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/discussions)
[![github/milestones](https://shields.io/github/milestones/all/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/milestones)
[![github/forks](https://shields.io/github/forks/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/network/members)
[![github/stars](https://shields.io/github/stars/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/stargazers)
[![github/watchers](https://shields.io/github/watchers/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/watchers)
[![github/contributors](https://shields.io/github/contributors/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/commits)
[![github/release-date](https://shields.io/github/release-date/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/releases/latest)

[![github/license](https://shields.io/github/license/rimeinn/pyrime)](https://github.com/rimeinn/pyrime/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)
[![github/languages/top](https://shields.io/github/languages/top/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)
[![github/directory-file-count](https://shields.io/github/directory-file-count/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)
[![github/code-size](https://shields.io/github/languages/code-size/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)
[![github/repo-size](https://shields.io/github/repo-size/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)
[![github/v](https://shields.io/github/v/release/rimeinn/pyrime)](https://github.com/rimeinn/pyrime)

[![pypi/status](https://shields.io/pypi/status/pyrime)](https://pypi.org/project/pyrime/#description)
[![pypi/v](https://shields.io/pypi/v/pyrime)](https://pypi.org/project/pyrime/#history)
[![pypi/downloads](https://shields.io/pypi/dd/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/format](https://shields.io/pypi/format/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/pyrime)](https://pypi.org/project/pyrime/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/pyrime)](https://pypi.org/project/pyrime/#files)

[![aur/votes](https://img.shields.io/aur/votes/python-pyrime)](https://aur.archlinux.org/packages/python-pyrime)
[![aur/popularity](https://img.shields.io/aur/popularity/python-pyrime)](https://aur.archlinux.org/packages/python-pyrime)
[![aur/maintainer](https://img.shields.io/aur/maintainer/python-pyrime)](https://aur.archlinux.org/packages/python-pyrime)
[![aur/last-modified](https://img.shields.io/aur/last-modified/python-pyrime)](https://aur.archlinux.org/packages/python-pyrime)
[![aur/version](https://img.shields.io/aur/version/python-pyrime)](https://aur.archlinux.org/packages/python-pyrime)

![screenshot](https://github.com/user-attachments/assets/5c79575c-79c5-4e4f-b6ab-b9cdaad352b2)

rime for python, attached to prompt-toolkit keybindings for some prompt-toolkit
applications such as ptpython.

## Dependence

- [librime](https://github.com/rime/librime)

```sh
# Ubuntu
sudo apt-get -y install librime-dev librime1 pkg-config
sudo apt-mark auto librime-dev pkg-config
# ArchLinux
sudo pacman -S --noconfirm librime pkg-config
# Android Termux
apt-get -y install librime pkg-config
# Nix
# use nix-shell to create a virtual environment then build
# homebrew
brew tap tonyfettes/homebrew-rime
brew install librime pkg-config
# Windows msys2
pacboy -S --noconfirm pkg-config librime gcc
```

## Configure

`~/.config/ptpython/config.py`:

```python
from ptpython.repl import PythonRepl
from prompt_toolkit.filters import EmacsInsertMode, ViInsertMode
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from pyrime.prompt_toolkit.rime import Rime


def configure(repl: PythonRepl) -> None:
    rime = Rime(repl)

    @repl.add_key_binding("c-^", filter=ViInsertMode())
    @repl.add_key_binding("c-^", filter=EmacsInsertMode())
    @repl.add_key_binding("c-^", filter=rime.mode())
    def _(event: KeyPressEvent) -> None:
        rime.toggle()
```

If you defined some key bindings which will disturb rime, try:

```python
    @repl.add_key_binding("c-h", filter=rime.filter(EmacsInsertMode()))
    def _(event: KeyPressEvent) -> None:
        rime.toggle()
```

If you want to exit rime in `ViNavigationMode()`, try:

```python
    @repl.add_key_binding("escape", filter=EmacsInsertMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.VI
        event.app.vi_state.input_mode = InputMode.NAVIGATION
        rime.conditional_disable()

    # and a, I, A, ...
    @repl.add_key_binding("i", filter=ViNavigationMode())
    def _(event: KeyPressEvent) -> None:
        """.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        rime.conditional_enable()
```

It will remember rime status and enable it when reenter `ViInsertMode()` or
`EmacsInsertMode()`.

Some utility functions are defined in this project. Refer
[my ptpython config](https://github.com/rimeinn/rimeinn/blob/main/.config/ptpython/config.py)
to know more.
