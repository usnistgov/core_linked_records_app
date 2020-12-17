""" System API for core_linked_records
"""
from core_linked_records_app.settings import PID_XPATH
from core_linked_records_app.utils.dict import get_dict_value_from_key_list
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data


def is_pid_defined_for_document(pid, document_id):
    """Determine if a given PID match the document ID provided.

    Params:
        pid:
        document_id:

    Returns:
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])

    return len(query_result) == 1 and query_result[0].pk == document_id


def is_pid_defined(pid):
    """Determine if a given PID already exists.

    Params:
        pid:

    Returns:
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])

    return len(query_result) == 1


def get_data_by_pid(pid):
    """Return data object with the given pid.

    Parameters:
        pid:

    Returns: data object
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])
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
    return get_dict_value_from_key_list(data["dict_content"], PID_XPATH.split("."))
