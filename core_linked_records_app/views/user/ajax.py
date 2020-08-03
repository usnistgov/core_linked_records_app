""" Ajax views accessible by users.
"""
import json

from django.http import JsonResponse
from django.views import View
from rest_framework import status

from core_linked_records_app.components.data.api import get_pids_for_data_list
from core_explore_common_app.components.query import api as query_api
from core_main_app.utils.requests_utils.requests_utils import (
    send_post_request,
    send_get_request,
)


class RetrievePID(View):
    """ Retrieve PIDs for a given list of data IDs.
    """

    def post(self, request):
        try:
            # FIXME duplicated code with core_explore_common.utils.query.send
            query = query_api.get_by_id(request.POST["query_id"])
            data_source = query.data_sources[int(request.POST["data_source_index"])]

            # Build serialized query to send to data source
            json_query = {
                "query": query.content,
                "templates": json.dumps(
                    [
                        {"id": str(template.id), "hash": template.hash}
                        for template in query.templates
                    ]
                ),
                "options": json.dumps(data_source.query_options),
                "order_by_field": data_source.order_by_field,
            }

            if "url_pid" not in data_source.capabilities.keys():
                return JsonResponse(
                    {"error": "The remote does not have PID capabilities."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response = send_get_request(
                data_source.capabilities["url_pid"],
                data=json_query,
                cookies={"sessionid": request.session.session_key},
            )

            if response.status_code == 200:
                return JsonResponse(
                    {"pids": response.json()}, status=response.status_code
                )
            else:
                return JsonResponse(
                    {
                        "error": "Remote service answered with status code %d."
                        % response.status_code
                    },
                    status=response.status_code,
                )
        except Exception as exception:
            return JsonResponse(
                {"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
