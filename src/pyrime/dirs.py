r"""Directories
===============
"""

import os

from platformdirs import user_data_path

shared_data_dir = ""
eprefix = os.getenv(
    "PREFIX",
    os.path.dirname(os.path.dirname(os.getenv("SHELL", "/bin/sh"))),
)
for prefix in [
    # /usr merge: /usr/bin/sh -> /usr/share/rime-data
    os.path.join(eprefix, "share"),
    # non /usr merge: /bin/sh -> /usr/share/rime-data
    os.path.join(eprefix, "usr/share"),
    "/run/current-system/sw",
    "/sdcard",
]:
    path = os.path.expanduser(os.path.join(prefix, "rime-data"))
    if os.path.isdir(path):
        shared_data_dir = path
        break

user_data_dir = ""
for prefix in [
    "~/.config/ibus",
    "~/.local/share/fcitx5",
    "~/.config/fcitx",
    "/sdcard",
]:
    path = os.path.expanduser(os.path.join(prefix, "rime"))
    if os.path.isdir(path):
        user_data_dir = path
        break

log_dir = str(user_data_path("ptpython") / "rime")
