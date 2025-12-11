r"""Test key."""

from prompt_toolkit.keys import Keys

from pyrime.key import Key
from pyrime.ptpython.bindings.rime import pt_key_name


class Test:
    r"""Test."""

    @staticmethod
    def test_parse_key() -> None:
        r"""Test parse key.

        :rtype: None
        """
        key = Key.new(pt_key_name((Keys.ControlCircumflex,)))
        assert key.basic == ord("6")
        assert key.modifier == key.modifier_flag.C
