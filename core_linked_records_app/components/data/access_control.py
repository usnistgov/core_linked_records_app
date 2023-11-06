""" Access control methods for `core_linked_records.components.data.api`.
"""
from core_main_app.access_control.api import check_can_read_document
from core_main_app.components.data.models import Data


def can_get_data_by_pid(func, pid, request):
    """Access control for the `get_data_by_pid` function.

    Args:
        func:
        pid:
        request:

    Returns:
    """
    data = func(pid, request)

    if not request.user.is_superuser:
        check_can_read_document(data, request.user)

    return data


def can_get_pid_for_data(func, data_id, request):
    """Access control for the `get_pid_for_data` function.

    Args:sel
        func:
        data_id:
        request:

    Returns:
    """
    if not request.user.is_superuser:
        check_can_read_document(Data.get_by_id(data_id), request.user)
    return func(data_id, request)
