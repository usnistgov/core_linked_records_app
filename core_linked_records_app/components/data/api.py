""" Local resolver API
"""
from core_linked_records_app.settings import PID_XPATH
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data.api import execute_query


def get_data_by_pid(request, pid):
    """ Return data object with the given pid.

        Parameters:
            pid:

        Returns: data object
    """
    json_pid_path = 'dict_content.' + PID_XPATH
    query_result = execute_query({json_pid_path: pid}, request.user)
    query_result_length = len(query_result)

    if query_result_length != 1:
        raise ApiError('Error: the PID must be unique' if query_result_length > 1 else 'Error: no results found')
    else:
        return query_result[0]