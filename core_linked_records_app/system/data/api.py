""" System API to manage Data objects.
"""
import logging

from django.conf import settings as conf_settings

from core_linked_records_app import settings
from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.system.pid_path.api import (
    get_pid_path_by_template,
)
from core_linked_records_app.utils.dict import get_value_from_dot_notation
from core_linked_records_app.utils.providers import delete_record_from_provider
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.query.mongo.prepare import sanitize_value

logger = logging.getLogger(__name__)


def is_pid_defined_for_data(pid, document_id):
    """Determine if a given PID match the document ID provided.

    Params:
        pid:
        document_id:

    Returns:
    """
    data = Data.get_by_id(document_id)

    pid_path_object = get_pid_path_by_template(data.template)
    pid_path = pid_path_object.path
    query = {
        f"dict_content__{pid_path.replace('.', '__')}__exact": sanitize_value(
            pid
        )
    }

    # pylint: disable=import-outside-toplevel
    if conf_settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q  # noqa
        from core_main_app.components.mongo.models import MongoData

        query_result = MongoData.execute_query(
            Q(**query),
            order_by_field=[],
        )
    else:
        from django.db.models import (
            Q,
        )

        query_result = Data.execute_query(
            Q(**query),
            order_by_field=[],
        )

    return len(query_result) == 1 and query_result[0].pk == document_id


def is_pid_defined(pid):
    """Determine if a given PID already exists.

    Params:
        pid:

    Returns:
    """
    try:
        get_data_by_pid(pid)
        return True
    except (DoesNotExist, ApiError):
        return False


def delete_pid_for_data(data: Data):
    """Deletes the PID assigned to the data passed in parameter. If no PID has
    been assigned, the function simply exits.

    Args:
        data: Data - The data for which the PID needs to be deleted.
    """
    # Retrieve the PID_PATH associated with the data template.
    pid_path_object = get_pid_path_by_template(data.template)
    pid_path = pid_path_object.path

    # Retrieve the data dict content to search for the PID_PATH using dot notation.
    try:  # Try to retrieve the dict content using data model
        dict_content = data.get_dict_content()
    except Exception:  # noqa, pylint: disable=broad-except
        # Retrieving the dict content is not possible, convert the xml to dict
        try:
            dict_content = xml_utils.raw_xml_to_dict(data.xml_content)
        except Exception as exc:  # Converting the xml to dict is not possible either
            raise ApiError(
                f"Impossible to retrieve the dict content for the data: {str(exc)}"
            ) from exc

    # Return PID value from the document and the PID_PATH
    current_pid = get_value_from_dot_notation(
        dict_content,
        pid_path,
    )

    if not current_pid:  # If there is no previous PID assigned.
        logger.info("No PID assigned to the data %s", str(data.pk))
        return

    # From the PID url (e.g. https://pid-system.org/prefix/record), retrieve
    # only the prefix and record (e.g. prefix/record) stored in DB.
    pid_internal_name = "/".join(current_pid.split("/")[-2:])

    # Delete the PID using the internal name.
    delete_record_from_provider(pid_internal_name)


def get_data_by_pid(pid):
    """Return data object with the given pid.

    Parameters:
        pid:

    Returns: data object
    """
    # pylint: disable=import-outside-toplevel
    if conf_settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q  # noqa
    else:
        from django.db.models import Q

    pid_path_query = Q(
        **{
            f"dict_content__{settings.PID_PATH.replace('.', '__')}__exact": sanitize_value(
                pid
            )
        }
    )

    # Create the or query with all the different PID path available.
    for pid_path_object in PidPath.get_all():
        pid_path_query |= Q(
            **{
                f"dict_content__{pid_path_object.path.replace('.', '__')}__exact": sanitize_value(
                    pid
                )
            }
        )
    # Execute built query and retrieve number of items returned.
    if conf_settings.MONGODB_INDEXING:
        from core_main_app.components.mongo.models import MongoData

        query_result = MongoData.execute_query(
            pid_path_query,
            order_by_field=[],
        )
    else:
        query_result = Data.execute_query(
            pid_path_query,
            order_by_field=[],
        )

    query_result_length = query_result.count()

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    if query_result_length != 1:
        raise ApiError("PID must be unique.")

    return query_result[0]
