r"""Wrap rime as OOP APIs."""

from dataclasses import dataclass
from typing import Self

from . import Commit, Context, SchemaListItem
from .__main__ import Traits
from ._C import (
    clear_composition,
    commit_composition,
    create_session,
    destroy_session,
    get_commit,
    get_context,
    get_current_schema,
    get_schema_list,
    init,
    process_key,
    select_schema,
)


@dataclass
class Rime:
    r"""Rime is a class to provide OOP APIs for librime."""

    session_id: int = 0

    @staticmethod
    def init(traits: Traits) -> None:
        r"""Init.

        :param traits:
        :type traits: Traits
        :rtype: None
        """
        init(**vars(traits))

    @staticmethod
    def create_session() -> int:
        r"""Create session.

        :rtype: int
        """
        return create_session()

    @classmethod
    def new(cls, traits: Traits) -> Self:
        r"""New.

        :param traits:
        :type traits: Traits
        :rtype: Self
        """
        cls.init(traits)
        return cls(cls.create_session())

    def process_key(self, keycode: int, mask: int) -> bool:
        r"""Process key.

        :param keycode:
        :type keycode: int
        :param mask:
        :type mask: int
        :rtype: bool
        """
        return process_key(self.session_id, keycode, mask)

    def get_context(self) -> Context | None:
        r"""Get context.

        :rtype: Context | None
        """
        return get_context(self.session_id)

    def get_commit(self) -> Commit | None:
        r"""Get commit.

        :rtype: Commit | None
        """
        return get_commit(self.session_id)

    def get_current_schema(self) -> str:
        r"""Get current schema.

        :rtype: str
        """
        return get_current_schema(self.session_id)

    @staticmethod
    def get_schema_list() -> list[SchemaListItem]:
        r"""Get schema list.

        :rtype: list[SchemaListItem]
        """
        return get_schema_list()

    def select_schema(self, schema_id: str) -> bool:
        r"""Select schema.

        :param schema_id:
        :type schema_id: str
        :rtype: bool
        """
        return select_schema(self.session_id, schema_id)

    def commit_composition(self) -> bool:
        r"""Commit composition.

        :rtype: bool
        """
        return commit_composition(self.session_id)

    def clear_composition(self) -> None:
        r"""Clear composition.

        :rtype: None
        """
        clear_composition(self.session_id)

    def __del__(self) -> None:
        r"""Del.

        :rtype: None
        """
        destroy_session(self.session_id)

    def get_commit_text(self) -> str:
        r"""Get commit text.

        :rtype: str
        """
        if self.commit_composition():
            commit = self.get_commit()
            if commit:
                return commit.text
        return ""
