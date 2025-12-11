r"""API
=======

Refer <https://github.com/rimeinn/rime.nvim/blob/main/lua/rime/traits.lua>
"""

import os
from dataclasses import dataclass

import cython as c
from cython.cimports.cpython.long import PyLong_AsVoidPtr, PyLong_FromVoidPtr
from cython.cimports.rime_api import (
    RimeApi,
    RimeCandidate,
    RimeCommit,
    RimeComposition,
    RimeContext,
    RimeMenu,
    RimeSchemaList,
    RimeSchemaListItem,
    RimeTraits,
    rime_get_api,
)
from platformdirs import site_data_dir, user_config_dir
from platformdirs import user_data_dir as _user_data_dir

from . import LogLevel, SchemaListItem, __version__
from . import __name__ as NAME
from .ime import (
    Candidate,
    Commit,
    Composition,
    Context,
    Menu,
)

@dataclass
class Traits:
    shared_data_dir: str = next(
        (
            dir
            for dir in site_data_dir("rime-data", multipath=True).split(":")
            if os.path.isdir(dir)
        ),
        "/sdcard/rime-data",
    )
    user_data_dir: str = next(
        (
            dir
            for dir in (
                user_config_dir("ibus", version="rime"),
                _user_data_dir("fcitx5", version="rime"),
                user_config_dir("fcitx", version="rime"),
            )
            if os.path.isdir(dir)
        ),
        "/sdcard/rime",
    )
    log_dir: str = _user_data_dir("ptpython", version="rime")
    distribution_name: str = "Rime"
    distribution_code_name: str = NAME
    distribution_version: str = __version__
    app_name: str = "rime." + NAME
    min_log_level: LogLevel = LogLevel.FATAL
    data_size: int = 0
    address: int = 0

    def __post_init__(self) -> None:
        r"""Initialize.
        gentoo prefix will change ``$XDG_DATA_DIRS``,
        TODO: Android termux only change ``$PREFIX``, not ``$XDG_DATA_DIRS``.
        Use trime data paths as the fallback of data directories.

        :param self:
        :rtype: None
        """
        for dir in self.shared_data_dir, self.user_data_dir, self.log_dir:
            if not os.path.isdir(dir):
                raise NotADirectoryError(dir)
        os.makedirs(self.log_dir, exist_ok=True)
        c_min_log_level: c.int = self.min_log_level.value
        traits: RimeTraits = RimeTraits(
            shared_data_dir=self.shared_data_dir.encode(),
            user_data_dir=self.user_data_dir.encode(),
            distribution_name=self.distribution_name.encode(),
            distribution_code_name=self.distribution_code_name.encode(),
            distribution_version=self.distribution_version.encode(),
            app_name=self.app_name.encode(),
            min_log_level=c_min_log_level,
            log_dir=self.log_dir.encode(),
        )
        traits.data_size = c.sizeof(RimeTraits) - c.sizeof(traits.data_size)
        self.data_size = traits.data_size
        self.address = PyLong_FromVoidPtr(c.address(traits))

        api: RimeApi = rime_get_api()[0]
        api.setup(c.address(traits))
        api.initialize(c.address(traits))

    def __del__(self) -> None:
        api: RimeApi = rime_get_api()[0]
        api.finalize()

@dataclass
class API:
    address: int = 0

    def __post_init__(self) -> None:
        r"""Get Rime API.

        :param self:
        :rtype: None
        """
        self.address: int = PyLong_FromVoidPtr(rime_get_api())

    def setup(self, traits: Traits) -> None:
        r"""Setup.

        :param self:
        :param traits:
        :type traits: Traits
        :rtype: None
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        p_traits: c.pointer[RimeTraits] = c.cast(
            c.pointer[RimeTraits], PyLong_AsVoidPtr(traits.address)
        )
        api.setup(p_traits)

    def initialize(self, traits: Traits) -> None:
        r"""Initialize. after ``setup()``.

        :param self:
        :param traits:
        :type traits: Traits
        :rtype: None
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        p_traits: c.pointer[RimeTraits] = c.cast(
            c.pointer[RimeTraits], PyLong_AsVoidPtr(traits.address)
        )
        api.initialize(p_traits)

    def finalize(self) -> int:
        r"""Finalize.

        :param self:
        :rtype: int
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.finalize()

    def create_session(self) -> int:
        r"""Create session.

        :param self:
        :rtype: int
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.create_session()

    def destroy_session(self, session_id: int) -> None:
        r"""Destroy session.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: None
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.destroy_session(session_id)

    def get_current_schema(self, session_id: int) -> str:
        r"""Get current schema.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: str
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        schema_id: c.char[1024] = c.declare(c.char[1024])  # type: ignore
        api.get_current_schema(session_id, schema_id, c.sizeof(schema_id))
        return schema_id.decode()

    def get_schema_list(self) -> list[SchemaListItem]:
        r"""Get schema list.

        :param self:
        :rtype: list[SchemaListItem]
        """
        schema_list: RimeSchemaList = c.declare(RimeSchemaList)
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        api.get_schema_list(c.address(schema_list))
        results: list[SchemaListItem] = []
        i: c.int
        for i in range(schema_list.size):
            schema: RimeSchemaListItem = schema_list.list[i]
            results += [
                SchemaListItem(
                    schema.schema_id.decode(),
                    schema.name.decode(),
                )
            ]
        return results

    def select_schema(self, session_id: int, schema_id: str) -> bool:
        r"""Select schema.

        :param self:
        :param session_id:
        :type session_id: int
        :param schema_id:
        :type schema_id: str
        :rtype: bool
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.select_schema(session_id, schema_id.encode()) == 1

    def process_key(self, session_id: int, keycode: int, mask: int) -> bool:
        r"""Process key.

        :param self:
        :param session_id:
        :type session_id: int
        :param keycode:
        :type keycode: int
        :param mask:
        :type mask: int
        :rtype: bool
        """
        _keycode: c.int = keycode
        _mask: c.int = mask
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.process_key(session_id, _keycode, _mask) == 1

    def get_context(self, session_id: int) -> Context | None:
        r"""Get context.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: Context | None
        """
        context: RimeContext = c.declare(RimeContext)
        context.data_size = c.sizeof(RimeContext) - c.sizeof(context.data_size)
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        if api.get_context(session_id, c.address(context)) != 1:
            return None
        composition: RimeComposition = context.composition
        preedit: str | None = (
            None
            if composition.preedit == c.NULL
            else composition.preedit.decode()
        )
        menu: RimeMenu = context.menu
        select_keys: str | None = (
            None if menu.select_keys == c.NULL else menu.select_keys.decode()
        )
        candidates: list[Candidate] = []
        i: c.int
        for i in range(menu.num_candidates):
            candidate: RimeCandidate = menu.candidates[i]
            comment: str | None = (
                None
                if candidate.comment == c.NULL
                else candidate.comment.decode()
            )
            candidates += [
                Candidate(
                    candidate.text.decode(),
                    comment,
                )
            ]
        return Context(
            Composition(
                c.cast(int, composition.length),
                c.cast(int, composition.cursor_pos),
                c.cast(int, composition.sel_start),
                c.cast(int, composition.sel_end),
                preedit,
            ),
            Menu(
                c.cast(int, menu.page_size),
                c.cast(int, menu.page_no),
                menu.is_last_page == 1,
                c.cast(int, menu.highlighted_candidate_index),
                c.cast(int, menu.num_candidates),
                select_keys,
                candidates,
            ),
        )

    def get_commit(self, session_id: int) -> Commit | None:
        r"""Get commit.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: Commit
        """
        commit: RimeCommit = c.declare(RimeCommit)
        commit.data_size = c.sizeof(RimeCommit) - c.sizeof(commit.data_size)
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        if api.get_commit(session_id, c.address(commit)) != 1:
            return None
        return Commit(commit.text.decode())

    def commit_composition(self, session_id: int) -> bool:
        r"""Commit composition.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: bool
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        return api.commit_composition(session_id) == 1

    def clear_composition(self, session_id: int) -> None:
        r"""Clear composition.

        :param self:
        :param session_id:
        :type session_id: int
        :rtype: None
        """
        api: RimeApi = c.cast(
            c.pointer[RimeApi], PyLong_AsVoidPtr(self.address)
        )[0]
        api.clear_composition(session_id)
