""" Local record API
"""
import logging

from core_main_app.commons import exceptions
from core_linked_records_app.components.local_id.models import LocalId

logger = logging.getLogger(__name__)


def get_by_name(record_name):
    """Retrieve the record by name.

    Args:
        record_name:

    Returns:
    """
    try:
        return LocalId.get_by_name(record_name)
    except exceptions.DoesNotExist as dne:
        raise exceptions.DoesNotExist(str(dne))
    except Exception as exc:
        error_message = "An unexpected error occurred while retrieving LocalId by name"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(f"{error_message}.")


def get_by_class_and_id(record_object_class, record_object_id):
    """Retrieve LocalID using linked object class and ID

    Args:
        record_object_class:
        record_object_id:

    Returns:
    """
    try:
        return LocalId.get_by_class_and_id(record_object_class, record_object_id)
    except exceptions.DoesNotExist as dne:
        raise exceptions.DoesNotExist(str(dne))
    except Exception as exc:
        error_message = (
            "An unexpected error occurred while retrieving LocalId by class and id"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(f"{error_message}.")


def insert(local_id_object):
    """Insert the record in the collection.

    Args:
        local_id_object:

    Returns:
    """
    try:
        LocalId.upsert(local_id_object)
        return local_id_object
    except Exception as exc:
        error_message = "An unexpected error occurred while inserting LocalId"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(f"{error_message}.")


def delete(local_id_object):
    """Delete the record.

    Args:
        local_id_object:

    Returns:

    """
    try:
        return local_id_object.delete()
    except Exception as exc:
        error_message = "An unexpected error occurred while deleting LocalId"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.ApiError(f"{error_message}.")
