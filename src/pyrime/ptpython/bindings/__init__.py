r"""Key Bindings
================

Refer
`<https://github.com/prompt-toolkit/python-prompt-toolkit/blob/3.0.52/src/prompt_toolkit/key_binding/bindings/default.py>`_
"""

from typing import TYPE_CHECKING

from prompt_toolkit.filters.base import Filter
from prompt_toolkit.key_binding.key_bindings import (
    KeyBindingsBase,
    merge_key_bindings,
)
from prompt_toolkit.keys import Keys

from .autoinsert import load_autoinsert_bindings
from .autopair import load_autopair_bindings
from .autosuggestion import load_autosuggestion_bindings
from .extra import load_extra_bindings
from .rime import load_rime_bindings
from .smartinput import load_smartinput_bindings
from .viemacs import load_viemacs_bindings

if TYPE_CHECKING:
    from ..ime import IME


def load_key_bindings(
    rime: "IME",
    keys_set: tuple[
        tuple[Keys | str, ...], ...
    ] = load_rime_bindings.__defaults__[0]
    if load_rime_bindings.__defaults__
    else (),
    insertions: dict[tuple[str, str], dict[tuple[Keys | str, ...], Filter]]
    | None = None,
) -> KeyBindingsBase:
    r"""Load key bindings.

    :param rime:
    :type rime: IME
    :param keys_set:
    :type keys_set: tuple[tuple[Keys | str, ...], ...]
    :param insertions:
    :type insertions: tuple[str, str], dict[tuple[Keys | str, ...], Filter]
                    | None
    :rtype: KeyBindingsBase
    """
    return merge_key_bindings([
        load_rime_bindings(rime, keys_set),
        load_autopair_bindings(rime),
        load_autosuggestion_bindings(rime),
        load_smartinput_bindings(rime),
        load_viemacs_bindings(rime),
        load_extra_bindings(rime),
        load_autoinsert_bindings(rime, insertions),
    ])
