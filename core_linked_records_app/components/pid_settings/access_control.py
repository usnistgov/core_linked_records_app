""" Access control methods for `core_linked_records.components.pid_settings.api`.
"""
from core_linked_records_app.access_control import rights
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.access_control.utils import check_has_perm


def can_upsert_pid_settings(func, pid_settings_object, user):
    """Access control for the `upsert` function.

    Args:
        func:
        pid_settings_object:
        user:

    Returns:
    """
    if user.is_superuser:
        return func(pid_settings_object, user)

    raise AccessControlError("The user cannot upsert PidSettings objects.")


def can_get_pid_settings(func, user):
    """Access control for the `get` function.

    Args:
        func:
        user:

    Returns:
    """
    check_has_perm(user, rights.CAN_READ_PID_SETTINGS)
    return func(user)
