""" Access control for `core_linked_records_app.components.blob.api`.
"""
from core_main_app.access_control.api import check_can_read_document
from core_main_app.components.blob.models import Blob


def can_get_blob_by_pid(func, pid, user):
    """Check that a user can retrieve a `Blob` from its PID.

    Args:
        func:
        pid:
        user:

    Raises:
        AccessControlError: The user does not have the proper permissions.

    Returns:
        Blob: Blob object to be returned by the function.
    """
    blob = func(pid, user)

    if not user.is_superuser:
        check_can_read_document(blob, user)
    return blob


def can_get_pid_for_blob(func, blob_id, user):
    """Check that a use can read a `Blob` from its id and retrieve the attached PID
    value.

    Args:
        func:
        blob_id:
        user:

    Raises:
        AccessControlError: The user does not have the proper permissions.

    Returns:
        any: Runs the function specified in parameters.
    """
    if not user.is_superuser:
        check_can_read_document(Blob.get_by_id(blob_id), user)
    return func(blob_id, user)


def can_set_pid_for_blob(func, blob_id, blob_pid, user):
    """Check that a user can assign a PID value a Blob object given its id.

    Args:
        func:
        blob_id:
        blob_pid:
        user:

    Raises:
        AccessControlError: The user does not have the proper permissions.

    Returns:
        any: Runs the function specified in parameters.
    """
    if not user.is_superuser:
        check_can_read_document(Blob.get_by_id(blob_id), user)
    return func(blob_id, blob_pid, user)
