""" Access control methods for `core_linked_records.components.oai_record.api`.
"""
from core_main_app.access_control.api import check_anonymous_access


def can_get_pid_for_data(func, oai_record_id, request):
    """Access control for the `get_pid_for_data` function.

    Args:
        func:
        oai_record_id:
        request:

    Returns:
    """
    check_anonymous_access(request.user)
    return func(oai_record_id, request)
