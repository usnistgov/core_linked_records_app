""" Local resolver API
"""
from logging import getLogger

from core_linked_records_app import settings
from core_linked_records_app.components.data.access_control import (
    can_get_pid_for_data,
    can_get_data_by_pid,
)
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.utils.dict import (
    is_dot_notation_in_dictionary,
    get_value_from_dot_notation,
)
from core_linked_records_app.utils.pid import is_valid_pid_value
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import ApiError, DoesNotExist
from core_main_app.components.data import api as data_api

logger = getLogger(__name__)


@access_control(can_get_data_by_pid)
def get_data_by_pid(pid, request):
    """Return data object with the given pid.

    Parameters:
        pid:
        request: HttpRequest

    Returns: data object
    """
    try:
        pid_path_list = [
            pid_path_object.path
            for pid_path_object in pid_path_api.get_all(request)
        ] + [settings.PID_PATH]
        dot_notation_pid_paths = [
            f"dict_content.{pid_path}" for pid_path in pid_path_list
        ]
        query_result = data_api.execute_json_query(
            {
                "$or": [
                    {dot_notation_pid_path: pid}
                    for dot_notation_pid_path in dot_notation_pid_paths
                ]
            },
            request.user,
        )
        query_result_length = len(query_result)
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up data assigned to PID '{pid}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.") from exc

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    if query_result_length != 1:
        raise ApiError("PID must be unique.")

    return query_result[0]


@access_control(can_get_pid_for_data)
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

        # Return PID value from the document and the pid_path retrieved from
        # `PidSettings`
        pid_path_object = pid_path_api.get_by_template(
            data.template, request.user
        )
        pid_path = pid_path_object.path

        # If the pid_path does not exist in the document, exit early and return None
        if not is_dot_notation_in_dictionary(
            data.get_dict_content(), pid_path
        ):
            return None

        pid_value = get_value_from_dot_notation(
            data.get_dict_content(), pid_path
        )

        # If the field has an invalid PID, raise an exception.
        if not is_valid_pid_value(
            pid_value, settings.ID_PROVIDER_SYSTEM_NAME, settings.PID_FORMAT
        ):
            raise ApiError(f"Invalid PID in data '{data_id}'")

        return pid_value
    except Exception as exc:
        error_message = (
            f"An error occurred while looking up PID assigned to data "
            f"'{data_id}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.") from exc
