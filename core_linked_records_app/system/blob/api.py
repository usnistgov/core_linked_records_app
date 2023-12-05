""" System API to manage  Blob objects.
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.system.local_id import api as local_id_system_api
from core_linked_records_app.utils.path import get_api_path_from_object
from core_linked_records_app.utils.providers import delete_record_from_provider
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.system.blob import api as blob_system_api

logger = logging.getLogger(__name__)


def get_pid_for_blob(blob_id):
    """Retrieve PID matching the blob ID provided.

    Args:
        blob_id:

    Raises:
        DoesNotExist: No PID found for the given Blob ID

    Returns:
        str - PID of the blob object
    """
    try:
        return local_id_system_api.get_by_class_and_id(
            record_object_class=get_api_path_from_object(Blob()),
            record_object_id=blob_id,
        )
    except exceptions.DoesNotExist as dne:
        raise exceptions.DoesNotExist(str(dne))
    except Exception as exc:
        error_message = f"An error occurred while looking up PID assigned to blob '{blob_id}'"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(error_message)


def set_pid_for_blob(blob_id, blob_pid):
    """Retrieve PID matching the blob ID provided.

    Args:
        blob_id:
        blob_pid:
    """
    try:
        record_name = (
            f"{settings.ID_PROVIDER_PREFIX_BLOB}/{blob_pid.split('/')[-1]}"
        )

        try:
            local_id_object = get_pid_for_blob(blob_id)
        except exceptions.DoesNotExist:
            try:
                local_id_object = local_id_system_api.get_by_name(record_name)
            except exceptions.DoesNotExist:
                local_id_object = None

        if local_id_object:
            local_id_object.record_name = record_name
            local_id_object.record_object_class = get_api_path_from_object(
                Blob()
            )
            local_id_object.record_object_id = str(blob_id)
        else:
            local_id_object = LocalId(
                record_name=record_name,
                record_object_class=get_api_path_from_object(Blob()),
                record_object_id=str(blob_id),
            )

        return local_id_system_api.insert(local_id_object)
    except Exception as exc:
        error_message = f"An error occurred while assigning PID '{blob_pid}' to blob '{blob_id}'"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(error_message)


def delete_pid_for_blob(blob: Blob):
    """Deletes the PID assigned to the blob passed in parameter. If no PID has
    been assigned, the function simply exits.

    Args:
        blob (Blob): The blob for which the PID needs to be deleted.
    """
    try:
        local_id_obj: LocalId = local_id_system_api.get_by_class_and_id(
            get_api_path_from_object(Blob()), blob.pk
        )

        # Delete the PID using the internal name.
        delete_record_from_provider(local_id_obj.record_name)
    except DoesNotExist:  # If there is no previous PID assigned.
        logger.info(
            "No PID assigned to the blob %s (%s). Skipping deletion.",
            str(blob.pk),
            blob.filename,
        )
        return


def get_blob_by_pid(pid):
    """Return blob object with the given pid.

    Args:
        pid (str): PID of the blob.

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
        if not (
            local_id_object.record_object_class
            and local_id_object.record_object_id
        ):
            raise exceptions.DoesNotExist("PID not assigned to blob")

        # Retrieve the blob object using the blob system API.
        # FIXME should be made more generic (using local_id_object.record_object_class)
        #  to retrieve any kind of object.
        return blob_system_api.get_by_id(local_id_object.record_object_id)
    except exceptions.DoesNotExist as not_assigned_exc:
        error_message = f"PID '{pid}' not assigned to blob"
        logger.error(error_message)
        raise exceptions.DoesNotExist(error_message) from not_assigned_exc
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up blob assigned to PID '{pid}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(error_message) from exc
