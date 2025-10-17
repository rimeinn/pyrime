"""
Gdb plugin for ptpython.

``~/.config/gdb/gdbinit``:

.. code-block:: gdb

    source ~/.config/gdb/gdbinit.py

``~/.config/gdb/gdbinit.py``:

.. code-block:: python

    from pyrime.ptpython.gdb import PtPythonCommand

    PtPythonCommand()

Then type ``ptpython``.

Refer `<https://github.com/prompt-toolkit/ptpython/issues/546>`_
"""

import os
import sys
from argparse import Namespace

import gdb  # type: ignore
from ptpython.entry_points.run_ptpython import get_config_and_history_file
from ptpython.repl import PythonRepl, embed, run_config

import __main__


class PtPythonCommand(gdb.Command):
    def __init__(self) -> None:
        super().__init__("ptpython", gdb.COMMAND_USER)
        a = Namespace(config_file=None, history_file=None)
        self.config_file, self.history_file = get_config_and_history_file(a)
        self.startup_paths = []
        if "PYTHONSTARTUP" in os.environ:
            self.startup_paths.append(os.environ["PYTHONSTARTUP"])

    def configure(self, repl: PythonRepl) -> None:
        if os.path.exists(self.config_file):
            run_config(repl, self.config_file)

    def invoke(self, argument: str, from_tty: bool):
        self.dont_repeat()

        if not from_tty:
            raise Exception("PtPython can only be launched from the TTY")

        stdout = sys.stdout
        stderr = sys.stderr
        stdin = sys.stdin

        try:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            sys.stdin = sys.__stdin__

            embed(  # type: ignore
                history_filename=self.history_file,
                configure=self.configure,
                locals=__main__.__dict__,
                globals=__main__.__dict__,
                startup_paths=self.startup_paths,
                title="GDB REPL (ptpython)",
            )

        except SystemExit as e:
            if e.code != 0:
                print("ptpython exited with code", e.code)

        finally:
            sys.stdout = stdout
            sys.stderr = stderr
            sys.stdin = stdin
