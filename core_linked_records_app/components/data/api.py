""" Local resolver API
"""
from logging import getLogger

from core_main_app.commons.exceptions import ApiError, DoesNotExist
from core_main_app.components.data import api as data_api
from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.utils.dict import (
    is_dot_notation_in_dictionary,
    get_value_from_dot_notation,
)
from core_linked_records_app.utils.pid import is_valid_pid_value

logger = getLogger(__name__)


def get_data_by_pid(pid, request):
    """Return data object with the given pid.

    Parameters:
        pid:
        request: HttpRequest

    Returns: data object
    """
    try:
        pid_xpath_list = [
            pid_xpath_object.xpath
            for pid_xpath_object in pid_xpath_api.get_all(request)
        ] + [settings.PID_XPATH]
        json_pid_xpaths = [f"dict_content.{pid_xpath}" for pid_xpath in pid_xpath_list]
        query_result = data_api.execute_json_query(
            {"$or": [{json_pid_xpath: pid} for json_pid_xpath in json_pid_xpaths]},
            request.user,
        )
        query_result_length = len(query_result)
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up data assigned to PID '{pid}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.")

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    if query_result_length != 1:
        raise ApiError("PID must be unique.")

    return query_result[0]


def get_pids_for_data_list(data_id_list, request):
    """Retrieve PID matching the document list provided.

    Args:
        data_id_list:
        request: HttpRequest

    Returns:
    """
    try:
        return [get_pid_for_data(data_id, request) for data_id in data_id_list]
    except Exception as exc:
        error_message = "An error occurred while retrieving PIDs for data list"

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.")


def get_pid_for_data(data_id, request):
    """Retrieve PID matching the document ID provided.

    Args:
        data_id:
        request: HttpRequest

    Returns:
    """
    try:
        # Retrieve the document passed as input and extra the PID field.
        data = data_api.get_by_id(data_id, request.user)

        # Return PID value from the document and the pid_xpath retrieved from
        # `PidSettings`
        pid_xpath_object = pid_xpath_api.get_by_template(data.template, request)
        pid_xpath = pid_xpath_object.xpath

        # If the pid_xpath does not exist in the document, exit early and return None
        if not is_dot_notation_in_dictionary(data.get_dict_content(), pid_xpath):
            return None

        pid_value = get_value_from_dot_notation(data.get_dict_content(), pid_xpath)

        # If the field has an invalid PID, raise an exception.
        if not is_valid_pid_value(
            pid_value, settings.ID_PROVIDER_SYSTEM_NAME, settings.PID_FORMAT
        ):
            raise ApiError(f"Invalid PID in data '{data_id}'")

        return pid_value
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up PID assigned to data '{data_id}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.")
