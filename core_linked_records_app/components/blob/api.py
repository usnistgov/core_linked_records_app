""" Local resolver Blob API.
"""
from importlib import import_module
from logging import getLogger

from core_linked_records_app.components.blob.access_control import (
    can_get_blob_by_pid,
    can_get_pid_for_blob,
    can_set_pid_for_blob,
)
from core_linked_records_app.system.blob import api as blob_system_api
from core_linked_records_app.system.local_id import api as local_id_system_api
from core_main_app.access_control.decorators import access_control
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions

logger = getLogger(__name__)


@access_control(can_get_blob_by_pid)
def get_blob_by_pid(pid, user):
    """Return blob object with the given pid.

    Args:
        pid (str): PID of the blob.
        user (User): User making the request, should have access to the Blob.

    Raises:
        DoesNotExist: The PID is not assigned to any Blob object.
        AccessControlError: The Blob cannot be accessed by the user.
        ApiError: Any other error occured while trying to resolve the PID.

    Returns:
        Blob: Blob object assigned to the given PID.
    """
    try:
        # From the PID url (e.g. https://pid-system.org/prefix/record), retrieve
        # only the prefix and record (e.g. prefix/record) stored in DB.
        pid_internal_name = "/".join(pid.split("/")[-2:])
        local_id_object = local_id_system_api.get_by_name(pid_internal_name)

        # Ensure the LocalID object refers to a Blob
        assert (
            local_id_object.record_object_class
            and local_id_object.record_object_id
        )

        # From the local ID object, retrieve record module, separating import path
        # and module name.
        record_object_classpath = local_id_object.record_object_class
        record_object_module_path = ".".join(
            record_object_classpath.split(".")[:-1]
        )
        api_module_name = record_object_classpath.split(".")[-1]

        # Import record module and call 'get_by_id' function with record ID as
        # parameter.
        module = import_module(record_object_module_path)
        return getattr(module, api_module_name).get_by_id(
            local_id_object.record_object_id, user
        )
    except (AssertionError, exceptions.DoesNotExist) as not_assigned_exc:
        error_message = f"PID '{pid}' not assigned to blob"
        logger.error(error_message)
        raise exceptions.DoesNotExist(error_message) from not_assigned_exc
    except AccessControlError as acl_error:
        logger.error(str(acl_error))
        raise AccessControlError(str(acl_error)) from acl_error
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up blob assigned to PID '{pid}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(error_message) from exc


@access_control(can_get_pid_for_blob)
def get_pid_for_blob(blob_id, user):  # noqa, pylint: disable=unused-argument
    """Retrieve PID matching the blob ID provided.

    Args:
        blob_id (str): Primary key of the Blob object.
        user (User): User making the request, should have access to the Blob object.

    Returns:
        str - PID of the blob object
    """
    return blob_system_api.get_pid_for_blob(blob_id)


@access_control(can_set_pid_for_blob)
def set_pid_for_blob(
    blob_id, blob_pid, user  # noqa, pylint: disable=unused-argument
):
    """Create a PID for the blob ID provided.

    Args:
        blob_id (str): Primary key of the Blob object.
        blob_pid (str): PID to assign to the Blob.
        user (User): User making the request, should have proper permissions to access
            the Blob and assign a PID

    Returns:
        LocalId: PID object created for the given Blob object.
    """
    return blob_system_api.set_pid_for_blob(blob_id, blob_pid)
