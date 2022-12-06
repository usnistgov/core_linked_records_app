""" System API for core_linked_records
"""
import logging

from django.conf import settings as conf_settings
from rest_framework import status

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.utils.dict import get_value_from_dot_notation
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data
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

    pid_xpath_object = get_pid_xpath_by_template(data.template)
    pid_xpath = pid_xpath_object.xpath
    query = {
        f"dict_content__{pid_xpath.replace('.', '__')}__exact": sanitize_value(
            pid
        )
    }

    if conf_settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q
        from core_main_app.components.mongo.models import MongoData

        query_result = MongoData.execute_query(
            Q(**query),
            order_by_field=[],
        )
    else:
        from django.db.models import Q

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


def get_data_by_pid(pid):
    """Return data object with the given pid.

    Parameters:
        pid:

    Returns: data object
    """
    if conf_settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q
    else:
        from django.db.models import Q

    pid_xpath_query = Q(
        **{
            f"dict_content__{settings.PID_XPATH.replace('.', '__')}__exact": sanitize_value(
                pid
            )
        }
    )

    # Create the or query with all the different PID Xpath available.
    for pid_xpath_object in PidXpath.get_all():
        pid_xpath_query |= Q(
            **{
                f"dict_content__{pid_xpath_object.xpath.replace('.', '__')}__exact": sanitize_value(
                    pid
                )
            }
        )
    # Execute built query and retrieve number of items returned.
    if conf_settings.MONGODB_INDEXING:
        from core_main_app.components.mongo.models import MongoData

        query_result = MongoData.execute_query(
            pid_xpath_query,
            order_by_field=[],
        )
    else:
        query_result = Data.execute_query(
            pid_xpath_query,
            order_by_field=[],
        )

    query_result_length = query_result.count()

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    if query_result_length != 1:
        raise ApiError("PID must be unique.")

    return query_result[0]


def get_pid_for_data(data_id):
    """Retrieve PID matching the document ID provided.

    Args:
        data_id:

    Returns:
    """
    # Retrieve the document passed as input and extra the PID field.
    data = Data.get_by_id(data_id)

    # Return PID value from the document and the PID_XPATH
    pid_xpath_object = get_pid_xpath_by_template(data.template)
    pid_xpath = pid_xpath_object.xpath

    return get_value_from_dot_notation(
        data.get_dict_content(),
        pid_xpath,
    )


def get_pid_xpath_by_template(template):
    """Retrieve XPath associated with a specific template ID

    Args:
        template: Template object

    Returns:
        PidXpath - PidXpath object, linking template ID and XPath
    """
    pid_xpath_object = PidXpath.get_by_template(template)

    if pid_xpath_object is None:
        return PidXpath(template=template, xpath=settings.PID_XPATH)

    return pid_xpath_object


def delete_pid_for_data(data):
    """Deletes the PID assigned to the data passed in parameter. If no PID has
    been assigned, the function simply exits.

    Args:
        data:
    """
    previous_pid = get_pid_for_data(data.pk)

    if not previous_pid:  # If there is no previous PID assigned.
        logger.info("No PID assigned to the data %s", str(data.pk))
        return

    provider = ProviderManager().get()  # Returns the default provider.

    # From the PID url (e.g. https://pid-system.org/prefix/record), retrieve
    # only the prefix and record (e.g. prefix/record) stored in DB.
    pid_internal_name = "/".join(previous_pid.split("/")[-2:])

    previous_pid_delete_response = provider.delete(pid_internal_name)

    # Log any error that happen during PID deletion.
    if previous_pid_delete_response.status_code != status.HTTP_200_OK:
        logger.warning(
            "Deletion of PID %s returned %s",
            previous_pid,
            previous_pid_delete_response.status_code,
        )
