r"""Session
===========

Wrap rime as OOP APIs.
Refer <https://github.com/rimeinn/rime.nvim/blob/main/lua/rime/session.lua>
"""

from dataclasses import dataclass, field

from . import SchemaListItem
from .api import API, Traits
from .ime import Commit, Context
from .utils import SessionBase


@dataclass
class Session(SessionBase):
    r"""A session for Rime"""

    traits: Traits = field(default_factory=Traits)
    api: API = field(default_factory=API)
    id: int = 0

    def __post_init__(self):
        r"""Post init.

        :param self:
        """
        if self.id == 0:
            self.id = self.api.create_session()

    def __del__(self) -> None:
        r"""Del.

        :param self:
        :rtype: None
        """
        self.api.destroy_session(self.id)

    def process_key(self, keycode: int, mask: int) -> bool:
        r"""Process key.

        :param self:
        :param keycode:
        :type keycode: int
        :param mask:
        :type mask: int
        :rtype: bool
        """
        return self.api.process_key(self.id, keycode, mask)

    def get_context(self) -> Context | None:
        r"""Get context.

        :param self:
        :rtype: Context | None
        """
        return self.api.get_context(self.id)

    def get_commit(self) -> Commit | None:
        r"""Get commit.

        :param self:
        :rtype: Commit | None
        """
        return self.api.get_commit(self.id)

    def get_current_schema(self) -> str:
        r"""Get current schema.

        :param self:
        :rtype: str
        """
        return self.api.get_current_schema(self.id)

    def get_schema_list(self) -> list[SchemaListItem]:
        r"""Get schema list.

        :param self:
        :rtype: list[SchemaListItem]
        """
        return self.api.get_schema_list()

    def select_schema(self, schema_id: str) -> bool:
        r"""Select schema.

        :param self:
        :param schema_id:
        :type schema_id: str
        :rtype: bool
        """
        return self.api.select_schema(self.id, schema_id)

    def commit_composition(self) -> bool:
        r"""Commit composition.

        :param self:
        :rtype: bool
        """
        return self.api.commit_composition(self.id)

    def clear_composition(self) -> None:
        r"""Clear composition.

        :param self:
        :rtype: None
        """
        self.api.clear_composition(self.id)

    def get_commit_text(self) -> str:
        r"""Get commit text.

        :param self:
        :rtype: str
        """
        if self.commit_composition():
            commit = self.get_commit()
            if commit:
                return commit.text
        return ""
