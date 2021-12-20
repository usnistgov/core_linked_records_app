""" Local resolver API
"""
from logging import getLogger

from django.db.models import Q

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.utils.dict import get_dict_value_from_key_list
from core_main_app.commons.exceptions import ApiError, DoesNotExist
from core_main_app.components.data import api as data_api

logger = getLogger(__name__)


def get_data_by_pid(pid, request):
    """Return data object with the given pid.

    Parameters:
        pid:
        request: HttpRequest

    Returns: data object
    """
    try:
        pid_xpath_query = Q(
            **{f"dict_content__{settings.PID_XPATH.replace('.', '__')}": pid}
        )

        # Create the or query with all the different PID Xpath available.
        for pid_xpath_object in pid_xpath_api.get_all(request):
            pid_xpath_query |= Q(
                **{f"dict_content__{pid_xpath_object.xpath.replace('.', '__')}": pid}
            )

        # Execute built query and retrieve number of items returned.
        query_result = data_api.execute_query(pid_xpath_query, request.user)
        query_result_length = len(query_result)
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up data assigned to PID '{pid}'"
        )

        logger.error(f"{error_message}: {str(exc)}")
        raise ApiError(f"{error_message}.")

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    elif query_result_length != 1:
        raise ApiError("PID must be unique.")
    else:
        return query_result[0]


def get_pids_for_data_list(data_id_list, request):
    """Retrieve PID matching the document list provided.

    Args:
        data_id_list:
        request: HttpRequest

    Returns:
    """
    try:
        # Retrieve the document passed as input and extra the PID field.
        data_list = data_api.get_by_id_list(data_id_list, request.user)

        # Build the list of PID from the document and the pid_xpath retrieve from the
        # `PidSettings`.
        pid_xpath_list = list()

        for data in data_list:
            pid_xpath_object = pid_xpath_api.get_by_template(data.template, request)
            pid_xpath_list.append((data, pid_xpath_object.xpath))

        pid_list = [
            get_dict_value_from_key_list(
                data.dict_content,
                pid_xpath.split("."),
            )
            for data, pid_xpath in pid_xpath_list
        ]

        # Returns a list of PID available from the list.
        return [pid for pid in pid_list if pid is not None]
    except Exception as exc:
        error_message = f"An error occurred while retrieving PIDs for data list"

        logger.error(f"{error_message}: {str(exc)}")
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

        return get_dict_value_from_key_list(data.dict_content, pid_xpath.split("."))
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up PID assigned to data '{data_id}'"
        )

        logger.error(f"{error_message}: {str(exc)}")
        raise ApiError(f"{error_message}.")
