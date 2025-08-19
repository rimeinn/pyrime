"""Ansi
=======

Convert ANSI escape code to prompt-toolkit class.

Experimental!

`<https://github.com/prompt-toolkit/ptpython/issues/525>`_
"""

import re
from functools import reduce

from colorama import Back, Fore, Style
from prompt_toolkit.formatted_text import AnyFormattedText

CODES = reduce(
    lambda x, y: x | y,
    map(
        lambda x: dict(
            (
                v,
                x[0]
                + k.lower()
                .replace("bright", "bold")
                .replace("dim", "italic")
                .replace(
                    "normal",
                    "nobold noitalic nounderline noblink noreverse nohidden"
                    " fg:white bg:black",
                )
                .replace("reset_all", "")
                .replace(
                    "reset", "black" if x[0].startswith("bg") else "white"
                )
                .replace("light", "bright")
                .replace("_ex", ""),
            )
            for k, v in vars(x[1]).items()
        ),
        {"fg:ansi": Fore, "bg:ansi": Back, "": Style}.items(),
    ),
)
PAT = re.compile("(" + "|".join(CODES).replace("[", "\\[") + ")")


def ansi2prompt_toolkit(
    ansi: str, prefix: str = ""
) -> tuple[AnyFormattedText, dict[str, str]]:
    """Ansi2prompt toolkit.

    :param ansi:
    :type ansi: str
    :param prefix:
    :type prefix: str
    :rtype: tuple[AnyFormattedText, dict[str, str]]
    """
    formats = []
    styles = {}
    num = 0
    class_name = prefix + str(num)
    text = ""
    style_name = ""
    for token in filter(len, PAT.split(ansi)):
        code_name = CODES.get(token)
        if code_name is None:
            text = token.replace("\n>>> ", "")
            formats += [("class:" + class_name, text)]
            styles |= {class_name: style_name}
            class_name += "." + str(num)
            text = ""
        if code_name == "":
            num += 1
            class_name = prefix + str(num)
            text = ""
        if code_name:
            style_name = code_name
            formats += [("class:" + class_name, text)]
            styles |= {class_name: style_name}
            class_name += "." + str(num)
            text = ""
    return formats, styles
