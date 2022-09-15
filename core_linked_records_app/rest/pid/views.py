""" Ajax views accessible by users.
"""
import json
from urllib.parse import urljoin

from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.utils.protocols.oauth2 import (
    send_post_request as oauth2_post_request,
    send_get_request as oauth2_get_request,
)
from core_main_app.utils.requests_utils.requests_utils import (
    send_get_request,
)
from core_linked_records_app import settings
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.data import api as data_api


class RetrieveDataPIDView(APIView):
    """Retrieve PIDs for a given data IDs."""

    def get(self, request):
        """get

        Args:
            request:

        Returns:
        """
        try:
            if "data_id" in request.GET:
                return JsonResponse(
                    {"pid": data_api.get_pid_for_data(request.GET["data_id"], request)}
                )
            if (
                "core_oaipmh_harvester_app" in settings.INSTALLED_APPS
                and "core_explore_oaipmh_app" in settings.INSTALLED_APPS
                and "oai_data_id" in request.GET
            ):
                from core_linked_records_app.components.oai_record import (
                    api as oai_record_api,
                )

                return JsonResponse(
                    {
                        "pid": oai_record_api.get_pid_for_data(
                            request.GET["oai_data_id"], request
                        )
                    }
                )
            if (
                "core_federated_search_app" in settings.INSTALLED_APPS
                and "fede_data_id" in request.GET
                and "fede_origin" in request.GET
            ):
                from core_federated_search_app.components.instance import (
                    api as instance_api,
                )

                fede_origin_keys = request.GET["fede_origin"].split("&")
                instance_name = fede_origin_keys[1].split("=")[1]
                instance = instance_api.get_by_name(instance_name)

                reverse_url = reverse("core_linked_records_retrieve_data_pid")
                url_get_data = f'{reverse_url}?data_id={request.GET["fede_data_id"]}'

                data_response = oauth2_get_request(
                    urljoin(instance.endpoint, url_get_data), instance.access_token
                )
                return JsonResponse(json.loads(data_response.text))

            return JsonResponse(
                {
                    "message": "Impossible to retrieve PID for data with the given "
                    "parameters"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            return JsonResponse(
                {
                    "message": f"An unexpected exception occurred while retrieving data "
                    f"PID: {str(exc)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveBlobPIDView(APIView):
    """Retrieve PIDs for a given blob ID."""

    def get(self, request):
        """get PIDs
        Args:
            request:

        Returns:

        """
        if "blob_id" in request.GET:
            try:
                blob_pid = blob_api.get_pid_for_blob(request.GET["blob_id"])
                sub_url = reverse(
                    "core_linked_records_provider_record",
                    kwargs={
                        "provider": settings.ID_PROVIDER_SYSTEM_NAME,
                        "record": "",
                    },
                )

                return JsonResponse(
                    {"pid": f"{settings.SERVER_URI}{sub_url}{blob_pid.record_name}"}
                )
            except Exception as exc:
                return JsonResponse(
                    {
                        "message": f"An unexpected exception occurred while retrieving "
                        f"blob PID: {str(exc)}"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return JsonResponse(
                {"message": "Missing parameter 'blob_id'."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrieveListPIDView(APIView):
    """Retrieve PIDs for a given list of data IDs."""

    def post(self, request):
        """get PIDs
        Args:
            request:

        Returns:

        """
        try:
            # FIXME duplicated code with core_explore_common.utils.query.send
            query = query_api.get_by_id(
                request.POST.get("query_id", None),
                request.user,
            )
            data_source = query.data_sources[
                int(request.POST.get("data_source_index", 0))
            ]

            # Build serialized query to send to data source
            json_query = {
                "query": query.content,
                "templates": json.dumps(
                    [
                        {"id": template.id, "hash": template.hash}
                        for template in query.templates.all()
                    ]
                ),
                "options": json.dumps(data_source["query_options"]),
                "order_by_field": data_source["order_by_field"],
            }

            if (
                "capabilities" in data_source.keys()
                and "url_pid" not in data_source["capabilities"].keys()
            ):
                return JsonResponse(
                    {"error": "The remote does not have PID capabilities."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if data_source["authentication"]["auth_type"] == "session":
                response = send_get_request(
                    data_source["capabilities"]["url_pid"],
                    json=json_query,
                    cookies={
                        "sessionid": request.session.session_key,
                    },
                )
            elif data_source["authentication"]["auth_type"] == "oauth2":
                response = oauth2_post_request(
                    data_source["capabilities"]["url_pid"],
                    json_query,
                    data_source["authentication"]["params"]["access_token"],
                    session_time_zone=timezone.get_current_timezone(),
                )
            else:
                raise Exception("Unknown authentication type.")

            if response.status_code == 200:
                return JsonResponse(
                    {"pids": [pid for pid in response.json() if pid is not None]},
                    status=response.status_code,
                )

            return JsonResponse(
                {
                    "error": f"Remote service answered with status code {response.status_code}."
                },
                status=response.status_code,
            )
        except Exception as exception:
            return JsonResponse(
                {"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
