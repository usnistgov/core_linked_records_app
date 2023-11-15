""" REST views for the query API
"""

from core_explore_common_app.rest.query.views import build_local_query
from core_linked_records_app import settings
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.utils.dict import get_value_from_dot_notation
from core_linked_records_app.utils.pid import is_valid_pid_value
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError, CoreError
from core_main_app.components.data import api as data_api


def build_pid_query(query, build_fn, request):
    """Build the query by adding an extra filter to limit to document with
    PID fields.

    Args:
        query:
        build_fn:
        request:

    Returns:
        Query with additional PID filter
    """
    query = build_fn(query)
    query = query["$and"] if "$and" in query.keys() else [query]

    # build PID query and append the raw query to it
    pid_path_list = [
        pid_path_object.path
        for pid_path_object in pid_path_api.get_all(request)
    ] + [settings.PID_PATH]
    pid_query = {
        "$and": [
            {
                "$or": [
                    {f"dict_content.{pid_path}": {"$exists": 1}}
                    for pid_path in pid_path_list
                ]
            }
        ]
        + query
    }

    return pid_query


def execute_pid_query(json_query, build_fn, execute_fn, request):
    """Build and execute a query given specific build and execute functions.

    Args:
        json_query:
        build_fn:
        execute_fn:
        request:

    Raises:
        AccessControlError
        ApiError

    Returns:
        Output of the execute function provided
    """
    try:
        # prepare query
        pid_query = build_pid_query(
            query=json_query, build_fn=build_fn, request=request
        )
        # execute query
        return execute_fn(pid_query, request)
    except AccessControlError as acl_error:
        raise AccessControlError(str(acl_error))
    except Exception as api_exception:
        raise ApiError(str(api_exception))


def execute_local_query(raw_query, request):
    """Execute the raw query in database

    Args:

        raw_query: Query to execute
        request:

    Returns:
        Results of the query
    """
    pid_list = list()
    data_list = data_api.execute_json_query(raw_query, request.user)

    for data in data_list:
        pid_path_object = pid_path_api.get_by_template(
            data.template, request.user
        )
        pid_path = pid_path_object.path

        data_pid = get_value_from_dot_notation(
            data.get_dict_content(),
            pid_path,
        )

        if not is_valid_pid_value(
            data_pid, settings.ID_PROVIDER_SYSTEM_NAME, settings.PID_FORMAT
        ):
            continue

        pid_list.append(data_pid)

    return pid_list


def execute_local_pid_query(json_query, request):
    """Execute a query to retrieve PIDs on data from a local data source.

    Args:
        json_query:
        request:

    Returns:
        Output of the `execute_local_query` function
    """
    return execute_pid_query(
        json_query, build_local_query, execute_local_query, request
    )


def execute_oaipmh_query(raw_query, request):
    """Execute the raw query in database

    Args:
        raw_query: Query to execute
        request:

    Returns:
        Results of the query
    """
    if "core_oaipmh_harvester_app" not in settings.INSTALLED_APPS:
        raise CoreError(
            "Missing dependency 'core_oaipmh_harvester_app' in INSTALLED_APPS"
        )

    from core_oaipmh_harvester_app.components.oai_record import (
        api as oai_record_api,
    )

    pid_list = list()
    data_list = oai_record_api.execute_json_query(raw_query, request.user)

    for data in data_list:
        pid_path_object = pid_path_api.get_by_template(
            data.harvester_metadata_format.template, request.user
        )
        pid_path = pid_path_object.path

        data_pid = get_value_from_dot_notation(
            data.get_dict_content(),
            pid_path,
        )

        if not data_pid:
            continue

        pid_list.append(data_pid)

    return pid_list


def execute_oaipmh_pid_query(json_query, request):
    """Execute a query to retrieve PIDs on data from a OAI-PMH data source.

    Args:
        json_query:
        request:

    Returns:
        Output of the `execute_oaipmh_query` function
    """
    if "core_explore_oaipmh_app" not in settings.INSTALLED_APPS:
        raise CoreError(
            "Missing dependency 'core_explore_oaipmh_app' in INSTALLED_APPS"
        )

    from core_explore_oaipmh_app.rest.query.views import build_oaipmh_query

    return execute_pid_query(
        json_query, build_oaipmh_query, execute_oaipmh_query, request
    )
