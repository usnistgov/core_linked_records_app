""" Local record API
"""
from mongoengine import NotUniqueError as MongoNotUniqueError

from core_linked_records_app.components.local_id.models import LocalId
from core_main_app.commons.exceptions import NotUniqueError


def get_by_name(record_name):
    """Retrieve the record by name.

    Args:
        record_name:

    Returns:
    """
    return LocalId.get_by_name(record_name)


def insert(record):
    """Insert the record in the collection.

    Args:
        record:

    Returns:
    """
    try:
        return record.save()
    except MongoNotUniqueError as e:
        raise NotUniqueError(e)


def delete(record):
    """Delete the record.

    Args:
        record:

    Returns:

    """
    return record.delete()
