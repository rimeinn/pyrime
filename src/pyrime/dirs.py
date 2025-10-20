r"""Directories
===============
"""

import os
from pathlib import Path
from typing import Any

from platformdirs import site_data_dir, user_config_path, user_data_path


def site_data_path(*args: Any, **kwargs: Any) -> tuple[Path, ...]:
    """`<https://github.com/tox-dev/platformdirs/issues/259>_`"""
    return tuple(
        Path(dir) for dir in site_data_dir(*args, **kwargs).split(":")
    )


# fallback for trime
shared_data_dir = "/sdcard"
eprefix = Path(
    os.getenv(
        "PREFIX",
        os.path.dirname(os.path.dirname(os.getenv("SHELL", "/bin/sh"))),
    )
)
for prefix in (  # /usr merge: /usr/bin/sh -> /usr/share/rime-data
    eprefix / "share",
    # non /usr merge: /bin/sh -> /usr/share/rime-data
    eprefix / "usr/share",
) + site_data_path(multipath=True):
    path = prefix / "rime-data"
    if path.is_dir():
        shared_data_dir = str(path)
        break

# fallback for trime
user_data_dir = "/sdcard"
for prefix in (
    user_config_path("ibus"),
    user_data_path("fcitx5"),
    user_config_path("fcitx"),
):
    path = prefix / "rime"
    if path.is_dir():
        user_data_dir = str(path)
        break

log_dir = str(user_data_path("ptpython") / "rime")
