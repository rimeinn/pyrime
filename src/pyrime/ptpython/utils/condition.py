r"""Filter
==========
"""

from prompt_toolkit.filters import Condition, EmacsInsertMode, ViInsertMode


def any_condition(*conditions: Condition) -> Condition:
    r"""Any condition.

    :param conditions:
    :type conditions: Condition
    :rtype: Condition
    """

    @Condition
    def _(conditions: tuple[Condition, ...] = conditions) -> bool:
        r""".

        :param conditions:
        :type conditions: tuple[Condition, ...]
        :rtype: bool
        """
        return any(condition() for condition in conditions)

    return _


def all_condition(*conditions: Condition) -> Condition:
    r"""All condition.

    :param conditions:
    :type conditions: Condition
    :rtype: Condition
    """

    @Condition
    def _(conditions: tuple[Condition, ...] = conditions) -> bool:
        r""".

        :param conditions:
        :type conditions: tuple[Condition, ...]
        :rtype: bool
        """
        return all(condition() for condition in conditions)

    return _


InsertMode = any_condition(EmacsInsertMode(), ViInsertMode())
