""" Local handle API
"""
from mongoengine import NotUniqueError as MongoNotUniqueError

from core_linked_records_app.components.handle.models import Handle
from core_main_app.commons.exceptions import NotUniqueError


def get_by_name(handle_name):
    """ Retrieve the handle by name.

    Args:
        handle_name:

    Returns:
    """
    handle_name = handle_name.lower()
    return Handle.get_by_name(handle_name)


def insert(handle):
    """ Insert the handle in the collection.

    Args:
        handle:

    Returns:
    """
    try:
        handle.handle_name = handle.handle_name.lower()
        return handle.save()
    except MongoNotUniqueError as e:
        raise NotUniqueError(e)


def delete(handle):
    """ Delete the handle.

    Args:
        handle:

    Returns:

    """
    return handle.delete()



