""" System API for core_linked_records
"""
from core_linked_records_app.settings import PID_XPATH
from core_main_app.components.data.models import Data


def is_pid_defined_for_document(pid, document_id):
    """ Determine if a given PID match the document ID provided.

    Params:
        pid:
        document_id:

    Returns:
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])

    return len(query_result) == 1 and query_result[0].pk == document_id


def is_pid_defined(pid):
    """ Determine if a given PID already exists.

    Params:
        pid:

    Returns:
    """
    json_pid_path = "dict_content.%s" % PID_XPATH
    query_result = Data.execute_query({json_pid_path: pid}, order_by_field=[])

    return len(query_result) == 1
