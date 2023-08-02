""" Linked records REST views
"""
import json
import logging

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app.components.blob.api import get_blob_by_pid
from core_linked_records_app.components.data.api import get_data_by_pid
from core_linked_records_app.rest.data.renderers.data_html_user_renderer import (
    DataHtmlUserRenderer,
)
from core_linked_records_app.rest.data.renderers.data_xml_renderer import (
    DataXmlRenderer,
)
from core_linked_records_app.utils.exceptions import (
    InvalidPrefixError,
    InvalidRecordError,
)
from core_linked_records_app.utils.pid import split_prefix_from_record
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.data.serializers import DataSerializer
from core_main_app.utils.file import get_file_http_response

logger = logging.getLogger(__name__)


class ProviderRecordView(APIView):
    """Provider Record View"""

    parser_classes = (JSONParser,)
    renderer_classes = (DataHtmlUserRenderer, JSONRenderer, DataXmlRenderer)

    def __init__(self, **kwargs):
        self.provider_manager = ProviderManager()
        super().__init__(**kwargs)

    def post(self, request, provider, record):
        """Create a handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        try:
            try:
                prefix, record = split_prefix_from_record(record)
            except InvalidPrefixError as invalid_prefix_error:
                return Response(
                    {
                        "record": record,
                        "url": request.build_absolute_uri("?"),
                        "message": str(invalid_prefix_error),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except InvalidRecordError as invalid_record_error:
                return Response(
                    {
                        "record": record,
                        "url": request.build_absolute_uri("?"),
                        "message": str(invalid_record_error),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            id_provider = self.provider_manager.get(provider)
            provider_response = id_provider.create(prefix, record)

            provider_content = json.loads(provider_response.content)
            return Response(
                provider_content, status=provider_response.status_code
            )
        except Exception as exc:  # pylint: disable=broad-except
            return Response(
                {
                    "record": record,
                    "url": request.build_absolute_uri("?"),
                    "message": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(
        self,
        request,  # noqa, pylint: disable=unused-argument
        provider,
        record,
    ):
        """Update the value of a given handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        try:
            id_provider = self.provider_manager.get(provider)
            provider_response = id_provider.update(record)

            provider_content = json.loads(provider_response.content)

            return Response(
                provider_content, status=provider_response.status_code
            )
        except Exception as exc:  # pylint: disable=broad-except
            return Response(
                {
                    "message": f"An unexpected error occurred while updating "
                    f"record: {str(exc)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, provider, record):
        """Retrieve the local data of a given handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        try:
            id_provider = self.provider_manager.get(provider)
            provider_response = id_provider.get(record)

            try:
                query_result = get_data_by_pid(
                    json.loads(provider_response.content)["url"], request
                )
                return Response(
                    DataSerializer(query_result).data,
                    status=status.HTTP_200_OK,
                )
            except DoesNotExist:
                # Try to find PID in blobs
                try:
                    query_result = get_blob_by_pid(
                        json.loads(provider_response.content)["url"],
                        request.user,
                    )

                    return get_file_http_response(
                        query_result.blob.read(), query_result.filename
                    )
                except AccessControlError as exception:
                    content = {"message": str(exception)}
                    return Response(content, status=status.HTTP_403_FORBIDDEN)
                except DoesNotExist:
                    content = {
                        "status": "error",
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": "No document with specified handle found",
                    }
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:  # pylint: disable=broad-except
            content = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(exc),
            }
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(
        self,
        request,  # noqa, pylint: disable=unused-argument
        provider,
        record,
    ):
        """Delete a handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        try:
            id_provider = self.provider_manager.get(provider)
            provider_response = id_provider.delete(record)

            provider_content = json.loads(provider_response.content)

            return Response(
                provider_content, status=provider_response.status_code
            )
        except Exception as exc:  # pylint: disable=broad-except
            return Response(
                {
                    "message": f"An unexpected error occurred while deleting "
                    f"record: {str(exc)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
