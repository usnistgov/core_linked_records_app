""" Local resolver API
"""
from core_linked_records_app.settings import PID_XPATH
from core_main_app.commons.exceptions import ApiError, DoesNotExist
from core_main_app.components.data import api as data_api


def get_data_by_pid(pid, user):
    """ Return data object with the given pid.

        Parameters:
            pid:
            user:

        Returns: data object
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = data_api.execute_query({json_pid_path: pid}, user)
    query_result_length = len(query_result)

    if query_result_length == 0:
        raise DoesNotExist("No result found")
    elif query_result_length != 1:
        raise ApiError("PID must be unique")
    else:
        return query_result[0]
