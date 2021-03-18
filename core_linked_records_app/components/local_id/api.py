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


def get_by_class_and_id(record_object_class, record_object_id):
    """Retrieve LocalID using linked object class and ID

    Args:
        record_object_class:
        record_object_id:

    Returns:
    """
    return LocalId.get_by_class_and_id(record_object_class, record_object_id)


def insert(local_id_object):
    """Insert the record in the collection.

    Args:
        local_id_object:

    Returns:
    """
    try:
        return local_id_object.save()
    except MongoNotUniqueError as e:
        raise NotUniqueError(e)


def delete(local_id_object):
    """Delete the record.

    Args:
        local_id_object:

    Returns:

    """
    return local_id_object.delete()
