"""cython file"""

import cython as c
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

from . import Candidate, Commit, Composition, Context, Menu, SchemaListItem

rime: RimeApi = c.declare(RimeApi)

def init(
    shared_data_dir: str = "/usr/share/rime-data",
    user_data_dir: str = "/root/.config/ibus/rime",
    log_dir: str = "/root/.local/share/ptpython/rime",
    distribution_name: str = "Rime",
    distribution_code_name: str = "pyrime",
    distribution_version: str = "0.0.1",
    app_name: str = "rime.pyrime",
    min_log_level: int = 3,
) -> None:
    r"""Init.

    :param shared_data_dir:
    :type shared_data_dir: str
    :param user_data_dir:
    :type user_data_dir: str
    :param log_dir:
    :type log_dir: str
    :param distribution_name:
    :type distribution_name: str
    :param distribution_code_name:
    :type distribution_code_name: str
    :param distribution_version:
    :type distribution_version: str
    :param app_name:
    :type app_name: str
    :param min_log_level:
    :type min_log_level: int
    :rtype: None
    """
    _min_log_level: c.int = min_log_level
    traits: RimeTraits = RimeTraits(
        shared_data_dir=shared_data_dir.encode(),
        user_data_dir=user_data_dir.encode(),
        distribution_name=distribution_name.encode(),
        distribution_code_name=distribution_code_name.encode(),
        distribution_version=distribution_version.encode(),
        app_name=app_name.encode(),
        min_log_level=_min_log_level,
        log_dir=log_dir.encode(),
    )
    traits.data_size = c.sizeof(RimeTraits) - c.sizeof(traits.data_size)
    global rime
    rime: RimeApi = rime_get_api()[0]
    rime.setup(c.address(traits))
    rime.initialize(c.address(traits))

def create_session() -> int:
    r"""Create session.

    :rtype: int
    """
    return rime.create_session()

def destroy_session(session_id: int) -> None:
    r"""Destroy session.

    :param session_id:
    :type session_id: int
    :rtype: None
    """
    return rime.destroy_session(session_id)

def get_current_schema(session_id: int) -> str:
    r"""Get current schema.

    :param session_id:
    :type session_id: int
    :rtype: str
    """
    schema_id: c.char[1024] = c.declare(c.char[1024])  # type: ignore
    rime.get_current_schema(session_id, schema_id, c.sizeof(schema_id))
    return schema_id.decode()

def get_schema_list() -> list[SchemaListItem]:
    r"""Get schema list.

    :rtype: list[SchemaListItem]
    """
    schema_list: RimeSchemaList = c.declare(RimeSchemaList)
    rime.get_schema_list(c.address(schema_list))
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

def select_schema(session_id: int, schema_id: str) -> bool:
    r"""Select schema.

    :param session_id:
    :type session_id: int
    :param schema_id:
    :type schema_id: str
    :rtype: bool
    """
    return rime.select_schema(session_id, schema_id.encode()) == 1

def process_key(session_id: int, keycode: int, mask: int) -> bool:
    r"""Process key.

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
    return rime.process_key(session_id, _keycode, _mask) == 1

def get_context(session_id: int) -> Context | None:
    r"""Get context.

    :param session_id:
    :type session_id: int
    :rtype: Context | None
    """
    context: RimeContext = c.declare(RimeContext)
    context.data_size = c.sizeof(RimeContext) - c.sizeof(context.data_size)
    if rime.get_context(session_id, c.address(context)) != 1:
        return None
    composition: RimeComposition = context.composition
    preedit: str | None = (
        None if composition.preedit == c.NULL else composition.preedit.decode()
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
            None if candidate.comment == c.NULL else candidate.comment.decode()
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

def get_commit(session_id: int) -> Commit | None:
    r"""Get commit.

    :param session_id:
    :type session_id: int
    :rtype: Commit
    """
    commit: RimeCommit = c.declare(RimeCommit)
    commit.data_size = c.sizeof(RimeCommit) - c.sizeof(commit.data_size)
    if rime.get_commit(session_id, c.address(commit)) != 1:
        return None
    return Commit(commit.text.decode())

def commit_composition(session_id: int) -> bool:
    r"""Commit composition.

    :param session_id:
    :type session_id: int
    :rtype: bool
    """
    return rime.commit_composition(session_id) == 1

def clear_composition(session_id: int) -> None:
    r"""Clear composition.

    :param session_id:
    :type session_id: int
    :rtype: None
    """
    rime.clear_composition(session_id)
