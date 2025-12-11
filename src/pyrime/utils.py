r"""Utils
=========
"""

from dataclasses import dataclass

from . import SchemaListItem
from .ime import Commit, Context


@dataclass
class SessionBase:
    r"""A dummy session."""

    def process_key(self, keycode: int, mask: int) -> bool:
        r"""Process key.

        :param self:
        :param keycode:
        :type keycode: int
        :param mask:
        :type mask: int
        :rtype: bool
        """
        return False

    def get_context(self) -> Context | None:
        r"""Get context.

        :param self:
        :rtype: Context | None
        """
        return None

    def get_commit(self) -> Commit | None:
        r"""Get commit.

        :param self:
        :rtype: Commit | None
        """
        return None

    def get_current_schema(self) -> str:
        r"""Get current schema.

        :param self:
        :rtype: str
        """
        return ""

    def get_schema_list(self) -> list[SchemaListItem]:
        r"""Get schema list.

        :param self:
        :rtype: list[SchemaListItem]
        """
        return []

    def select_schema(self, schema_id: str) -> bool:
        r"""Select schema.

        :param self:
        :param schema_id:
        :type schema_id: str
        :rtype: bool
        """
        return False

    def commit_composition(self) -> bool:
        r"""Commit composition.

        :param self:
        :rtype: bool
        """
        return False

    def clear_composition(self) -> None:
        r"""Clear composition.

        :param self:
        :rtype: None
        """

    def get_commit_text(self) -> str:
        r"""Get commit text.

        :param self:
        :rtype: str
        """
        return ""
