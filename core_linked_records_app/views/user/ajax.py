""" Ajax views accessible by users.
"""
import json

from django.http import JsonResponse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from rest_framework import status

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.utils.protocols.oauth2 import (
    send_post_request as oauth2_request,
)
from core_linked_records_app.components.data import api as data_api
from core_linked_records_app.components.oai_record import api as oai_record_api
from core_main_app.utils.requests_utils.requests_utils import send_get_request


class RetrieveDataPID(View):
    """Retrieve PIDs for a given data IDs."""

    def post(self, request):
        try:
            return JsonResponse(
                {
                    "pid": data_api.get_pid_for_data(
                        request.POST["data_id"], request.user
                    )
                }
            )
        except MultiValueDictKeyError:  # data_id key doesn't exist in request.POST
            return JsonResponse(
                {"pid": oai_record_api.get_pid_for_data(request.POST["oai_data_id"])}
            )


class RetrieveListPID(View):
    """Retrieve PIDs for a given list of data IDs."""

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

            if (
                getattr(data_source, "capabilities", False)
                and "url_pid" not in data_source.capabilities.keys()
            ):
                return JsonResponse(
                    {"error": "The remote does not have PID capabilities."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if data_source.authentication.type == "session":
                response = send_get_request(
                    data_source.capabilities["url_pid"],
                    data=json_query,
                    cookies={"sessionid": request.session.session_key},
                )
            elif data_source.authentication.type == "oauth2":
                response = oauth2_request(
                    data_source.capabilities["url_pid"],
                    json_query,
                    data_source.authentication.params["access_token"],
                    session_time_zone=timezone.get_current_timezone(),
                )
            else:
                raise Exception("Unknown authentication type.")

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
