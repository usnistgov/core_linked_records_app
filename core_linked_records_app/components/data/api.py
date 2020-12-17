""" Local resolver API
"""

from core_linked_records_app.settings import PID_XPATH
from core_linked_records_app.utils.dict import get_dict_value_from_key_list
from core_main_app.commons.exceptions import ApiError, DoesNotExist
from core_main_app.components.data import api as data_api


def get_data_by_pid(pid, user):
    """Return data object with the given pid.

    Parameters:
        pid:
        user:

    Returns: data object
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = data_api.execute_query({json_pid_path: pid}, user)
    query_result_length = len(query_result)

    if query_result_length == 0:
        raise DoesNotExist("PID is not attached to any data.")
    elif query_result_length != 1:
        raise ApiError("PID must be unique.")
    else:
        return query_result[0]


def get_pids_for_data_list(data_id_list, user):
    """Retrieve PID matching the document list provided.

    Args:
        data_id_list:
        user:

    Returns:
    """

    # Retrieve the document passed as input and extra the PID field.
    data_list = data_api.get_by_id_list(data_id_list, user)

    # Build the list of PID from the document and the PID_XPATH
    pid_list = [
        get_dict_value_from_key_list(data["dict_content"], PID_XPATH.split("."))
        for data in data_list
    ]

    # Returns a list of PID available from the list.
    return [pid for pid in pid_list if pid is not None]


def get_pid_for_data(data_id, user):
    """Retrieve PID matching the document ID provided.

    Args:
        data_id:
        user:

    Returns:
    """
    # Retrieve the document passed as input and extra the PID field.
    data = data_api.get_by_id(data_id, user)

    # Return PID value from the document and the PID_XPATH
    return get_dict_value_from_key_list(data["dict_content"], PID_XPATH.split("."))
