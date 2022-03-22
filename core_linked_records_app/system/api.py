""" System API for core_linked_records
"""
import logging
from rest_framework import status

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.utils.dict import get_dict_value_from_key_list
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data
from core_main_app.utils.requests_utils.requests_utils import send_delete_request

logger = logging.getLogger(__name__)


def is_pid_defined_for_document(pid, document_id):
    """Determine if a given PID match the document ID provided.

    Params:
        pid:
        document_id:

    Returns:
    """
    data = Data.get_by_id(document_id)

    pid_xpath_object = get_pid_xpath_by_template_id(data.template.pk)
    pid_xpath = pid_xpath_object.xpath

    json_pid_path = f"dict_content.{pid_xpath}"
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])

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
    pid_xpath_list = [
        pid_xpath_object.xpath for pid_xpath_object in PidXpath.get_all()
    ] + [settings.PID_XPATH]
    json_pid_xpaths = [f"dict_content.{pid_xpath}" for pid_xpath in pid_xpath_list]
    query_result = Data.execute_query(
        {"$or": [{json_pid_xpath: pid} for json_pid_xpath in json_pid_xpaths]},
        order_by_field=[],
    )
    query_result_length = len(query_result)

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    elif query_result_length != 1:
        raise ApiError("PID must be unique.")
    else:
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
    pid_xpath_object = get_pid_xpath_by_template_id(data.template.pk)
    pid_xpath = pid_xpath_object.xpath

    return get_dict_value_from_key_list(
        data["dict_content"],
        pid_xpath.split("."),
    )


def get_pid_xpath_by_template_id(template_id):
    """Retrieve XPath associated with a specific template ID

    Args:
        template_id: ObjectId

    Returns:
        PidXpath - PidXpath object, linking template ID and XPath
    """
    pid_xpath_object = PidXpath.get_by_template_id(template_id)

    if pid_xpath_object is None:
        return PidXpath(template=template_id, xpath=settings.PID_XPATH)
    else:
        return pid_xpath_object


def delete_pid_for_data(data):
    """Deletes the PID assigned to the data passed in parameter. If no PID has
    been assigned, the function simply exits.

    Args:
        data:
    """
    provider_manager = ProviderManager()
    previous_pid = get_pid_for_data(data.pk)

    if previous_pid is None:  # If there is no previous PID assigned
        logger.info(f"No PID assigned to the data {str(data.pk)}")
        return

    previous_provider_name = provider_manager.find_provider_from_pid(previous_pid)
    previous_provider = provider_manager.get(previous_provider_name)
    previous_pid_url = previous_pid.replace(
        previous_provider.provider_lookup_url, previous_provider.local_url
    )

    previous_pid_delete_response = send_delete_request(
        "%s?format=json" % previous_pid_url
    )

    # Log any error that happen during PID deletion
    if previous_pid_delete_response.status_code != status.HTTP_200_OK:
        logger.warning(
            "Deletion of PID %s returned %s"
            % (previous_pid, previous_pid_delete_response.status_code)
        )
