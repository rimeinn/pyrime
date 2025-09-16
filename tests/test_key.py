r"""Test key."""

from pyrime.key import Key, ModifierKey


class Test:
    r"""Test."""

    @staticmethod
    def test_parse_key() -> None:
        r"""Test parse key.

        :rtype: None
        """
        key = Key.new(("c-^",))
        assert key.basic.value == ord("6")
        assert key.modifier == ModifierKey.Control

    @staticmethod
    def test_get_ansi() -> None:
        r"""Test ANSI escape code.

        :rtype: None
        """
        assert (
            ModifierKey.Control | ModifierKey.Shift | ModifierKey.Alt
        ).get_ansi() == 8
        assert (
            ModifierKey.Control | ModifierKey.Shift | ModifierKey.Alt
        ) == ModifierKey.from_ansi(8)

    @staticmethod
    def test_ansi() -> None:
        r"""Test ANSI escape code.

        :rtype: None
        """
        key = Key.new(
            "enter", ModifierKey.Control | ModifierKey.Shift | ModifierKey.Alt
        )
        assert key.keys == ("escape", *"[27;8;13~")
        assert key == Key.new(("escape", *"[27;8;13~"))
