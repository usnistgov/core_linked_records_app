""" Local resolver Blob API.
"""
from importlib import import_module

from core_linked_records_app import settings
from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.utils.path import get_api_path_from_object
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.blob.models import Blob


def get_blob_by_pid(pid, user):
    """Return blob object with the given pid.

    Args:
        pid:
        user:

    Returns:
        Blob object
    """
    # From the PID url (e.g. https://pid-system.org/prefix/record), retrieve
    # only the prefix and record (e.g. prefix/record) stored in DB.
    pid_internal_name = "/".join(pid.split("/")[-2:])
    local_id_object = local_id_api.get_by_name(pid_internal_name)

    # From the local ID object, retrieve record module, separating import path
    # and module name.
    record_object_classpath = local_id_object.record_object_class
    record_object_module_path = ".".join(record_object_classpath.split(".")[:-1])
    api_module_name = record_object_classpath.split(".")[-1]

    # Import record module and call 'get_by_id' function with record ID as
    # parameter.
    module = import_module(record_object_module_path)
    return getattr(module, api_module_name).get_by_id(
        local_id_object.record_object_id, user
    )


def get_pid_for_blob(blob_id):
    """Retrieve PID matching the blob ID provided.

    Args:
        blob_id:

    Returns:
        str - PID of the blob object
    """
    return local_id_api.get_by_class_and_id(
        record_object_class=get_api_path_from_object(Blob()),
        record_object_id=blob_id,
    )


def set_pid_for_blob(blob_id, blob_pid):
    """Retrieve PID matching the blob ID provided.

    Args:
        blob_id:
        blob_pid:
    """
    record_name = f"{settings.ID_PROVIDER_PREFIX_BLOB}/{blob_pid.split('/')[-1]}"

    try:
        local_id_object = get_pid_for_blob(blob_id)
    except exceptions.DoesNotExist:
        try:
            local_id_api.get_by_name(record_name)
            raise ApiError(f"PID {blob_pid} is already assigned.")
        except exceptions.DoesNotExist:
            local_id_object = None

    if local_id_object:
        local_id_object.record_name = record_name
        local_id_object.record_object_class = get_api_path_from_object(Blob())
        local_id_object.record_object_id = str(blob_id)
    else:
        local_id_object = LocalId(
            record_name=record_name,
            record_object_class=get_api_path_from_object(Blob()),
            record_object_id=str(blob_id),
        )

    return local_id_api.insert(local_id_object)