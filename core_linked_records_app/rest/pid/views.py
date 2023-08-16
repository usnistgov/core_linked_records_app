""" Ajax views accessible by users.
"""
import json
from urllib.parse import urljoin

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.utils.oaipmh import oaipmh as oaipmh_utils
from core_explore_common_app.utils.protocols.oauth2 import (
    send_post_request as oauth2_post_request,
    send_get_request as oauth2_get_request,
)
from core_explore_common_app.utils.query import query as query_utils
from core_linked_records_app import settings
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.data import api as data_api
from core_linked_records_app.utils.query import execute_local_pid_query

if (
    "core_oaipmh_harvester_app" in settings.INSTALLED_APPS
    and "core_explore_oaipmh_app" in settings.INSTALLED_APPS
):  # Import OAI-PMH pid views if packages are present.
    from core_linked_records_app.utils.query import (
        execute_oaipmh_pid_query,
    )


class RetrieveDataPIDView(APIView):
    """Retrieve PIDs for a given data IDs."""

    def get(self, request):
        """get

        Args:
            request:

        Returns:
        """
        try:
            if "data_id" in request.GET:  # Local data
                return Response(
                    {
                        "pid": data_api.get_pid_for_data(
                            request.GET["data_id"], request
                        )
                    }
                )
            if (
                "core_oaipmh_harvester_app" in settings.INSTALLED_APPS
                and "core_explore_oaipmh_app" in settings.INSTALLED_APPS
                and "oai_data_id" in request.GET
            ):  # OAI-PMH data
                from core_linked_records_app.components.oai_record import (
                    api as oai_record_api,
                )

                return Response(
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
            ):  # Federated data
                from core_federated_search_app.components.instance import (
                    api as instance_api,
                )

                fede_origin_keys = request.GET["fede_origin"].split("&")
                instance_name = fede_origin_keys[1].split("=")[1]
                instance = instance_api.get_by_name(instance_name)

                reverse_url = reverse("core_linked_records_retrieve_data_pid")
                url_get_data = (
                    f'{reverse_url}?data_id={request.GET["fede_data_id"]}'
                )

                data_response = oauth2_get_request(
                    urljoin(instance.endpoint, url_get_data),
                    instance.access_token,
                )
                return Response(json.loads(data_response.text))

            return Response(
                {
                    "message": "Impossible to retrieve PID for data with the given "
                    "parameters"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            return Response(
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
                blob_pid = blob_api.get_pid_for_blob(
                    request.GET["blob_id"], request.user
                )
                sub_url = reverse(
                    "core_linked_records_provider_record",
                    kwargs={
                        "provider": settings.ID_PROVIDER_SYSTEM_NAME,
                        "record": "",
                    },
                )

                return Response(
                    {
                        "pid": f"{settings.SERVER_URI}{sub_url}{blob_pid.record_name}"
                    }
                )
            except Exception as exc:
                return Response(
                    {
                        "message": f"An unexpected exception occurred while retrieving "
                        f"blob PID: {str(exc)}"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"message": "Missing parameter 'blob_id'."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrieveListPIDView(APIView):
    """Retrieve PIDs for a given list of data IDs."""

    def post(self, request):
        """Retrieve PIDs
        Args:
            request:

        Returns:

        """
        try:
            # FIXME duplicated code with core_explore_common.utils.query.send
            query = query_api.get_by_id(
                request.data.get("query_id", None),
                request.user,
            )
            data_source = query.data_sources[
                int(request.data.get("data_source_index", 0))
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
                data_source["authentication"]["auth_type"] == "session"
            ):  # Local and OAI-PMH data sources
                if query_utils.is_local_data_source(data_source):
                    json_response = execute_local_pid_query(
                        json_query, request
                    )
                elif oaipmh_utils.is_oai_data_source(data_source):

                    json_response = execute_oaipmh_pid_query(
                        json_query, request
                    )
                else:
                    raise ExploreRequestError("Unknown data source type.")
            elif (
                data_source["authentication"]["auth_type"] == "oauth2"
            ):  # Federated data sources
                response = oauth2_post_request(
                    data_source["capabilities"]["query_pid"],
                    json_query,
                    data_source["authentication"]["params"]["access_token"],
                    session_time_zone=timezone.get_current_timezone(),
                )

                if response.status_code == status.HTTP_200_OK:
                    json_response = response.json()
                else:
                    return Response(
                        {
                            "error": f"Data source returned HTTP {response.status_code}."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Unknown authentication type."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"pids": [pid for pid in json_response if pid is not None]},
                status=status.HTTP_200_OK,
            )
        except Exception as exception:
            return Response(
                {"error": str(exception)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
