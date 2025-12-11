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

This project is consist of two parts:

- A python binding of librime
- A librime frontend on ptpython
- A librime frontend on neovim (TODO)

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
brew install librime pkg-config
# Windows msys2
pacboy -S --noconfirm pkg-config librime gcc
```

## Usage

### Binding

```python
from pyrime.ime.ui import UI
from pyrime.key import Key
from pyrime.session import Session

session = Session()
key = Key.new("n")
ui = UI()
if not session.process_key(key.code, key.mask):
    raise Exception
context = session.get_context()
if context is None:
    raise Exception
content, _ = ui.draw(context)
print("\n".join(content))
```

```text
n|
[① 你]② 那 ③ 呢 ④ 能 ⑤ 年 ⑥ 您 ⑦ 内 ⑧ 拿 ⑨ 哪 ⓪ 弄 |>
```

A simplest example can be found by:

```sh
pip install pyrime[cli]
python -m pyrime
```

By default, pyrime search ibus/fcitx/trime's config paths. You can see where it
found:

```python
from pyrime.api import Traits

print(Traits.user_data_dir)
```

### Frontend

`~/.config/ptpython/config.py`:

```python
from ptpython.repl import PythonRepl
from prompt_toolkit.filters.app import (
    emacs_insert_mode,
    vi_insert_mode,
    vi_navigation_mode,
)
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from pyrime.ptpython.rime import Rime


def configure(repl: PythonRepl) -> None:
    rime = Rime(repl)

    @repl.add_key_binding("c-^", filter=rime.insert_mode)
    def _(event: KeyPressEvent) -> None:
        rime.is_enabled = not rime.is_enabled
```

If you have a special rime config path, you can:

```python
import os

from ptpython.repl import PythonRepl
from pyrime.session import Session
from pyrime.api import Traits


def configure(repl: PythonRepl) -> None:

    rime = Rime(
        repl,
        Session(Traits(user_config_dir=os.path.expanduser("~/.config/rime"))),
    )
```

If you have defined some key bindings which will disturb rime, try:

```python
    @repl.add_key_binding("c-h", filter=emacs_insert_mode & ~rime.preedit_available())
    def _(event: KeyPressEvent) -> None:
        pass
```

If you want to exit rime in `vi_navigation_mode`, refer the following code of
`pyrime.ptpython.bindings.viemacs`'s `load_viemacs_bindings()`:

```python
    @repl.add_key_binding("escape", filter=rime.insert_mode)
    def _(event: KeyPressEvent) -> None:
        """Switch insert mode to normal mode.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        # store rime status
        rime.iminsert = rime.is_enabled
        # disable rime
        rime.is_enabled = False
        event.app.editing_mode = EditingMode.VI
        event.app.vi_state.input_mode = InputMode.NAVIGATION

    # and a, I, A, ...
    @repl.add_key_binding("i", filter=vi_navigation_mode)
    def _(event: KeyPressEvent) -> None:
        """Switch normal mode to insert mode.

        :param event:
        :type event: KeyPressEvent
        :rtype: None
        """
        event.app.editing_mode = EditingMode.EMACS
        event.app.vi_state.input_mode = InputMode.INSERT
        # recovery rime status
        rime.is_enabled = rime.iminsert
```

It will remember rime status and enable it when reenter `vi_insert_mode` or
`emacs_insert_mode`.

Some predefined key bindings are
[provided](https://github.com/rimeinn/pyrime/tree/main/src/pyrime/ptpython/bindings).
You can enable what you want:

```python
from prompt_toolkit.key_binding.key_bindings import merge_key_bindings
from pyrime.ptpython.bindings.autopair import load_autopair_bindings
from pyrime.ptpython.bindings.rime import load_rime_bindings

# by default, last registry is:
# from pyrime.ptpython.bindings import load_key_bindings
# rime.app.key_bindings.registries[-1] = load_key_bindings(rime)
rime.app.key_bindings.registries[-1] = merge_key_bindings([
    load_rime_bindings(rime),
    load_autopair_bindings(rime),
])
```

## Related Projects

- [A collection](https://github.com/rime/librime#frontends) of rime frontends
- [A collection](https://github.com/rimeinn/ime.nvim/#librime) of rime frontends
  for neovim
- [A collection](https://github.com/rimeinn/rime.nvim#translators-and-filters)
  of rime translators and filters
