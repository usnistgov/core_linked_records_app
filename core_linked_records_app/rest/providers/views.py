""" Linked records REST views
"""
import json
import logging
import re

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app import settings
from core_linked_records_app.components.data.api import get_data_by_pid
from core_linked_records_app.rest.data.renderers.data_html_user_renderer import (
    DataHtmlUserRenderer,
)
from core_linked_records_app.rest.data.renderers.data_xml_renderer import (
    DataXmlRenderer,
)
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.data.serializers import DataSerializer

LOGGER = logging.getLogger(__name__)


class ProviderRecord(APIView):
    parser_classes = (JSONParser,)
    renderer_classes = (DataHtmlUserRenderer, JSONRenderer, DataXmlRenderer)

    def __init__(self):
        self.provider_manager = ProviderManager()
        super().__init__()

    def post(self, request, provider, record):
        """Create a handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        # Parse record entry to split between prefix and record ID.
        prefix_record_list = record.split("/")

        if len(prefix_record_list) == 1:  # No record provided
            prefix = prefix_record_list[0]
            record = None
        elif prefix_record_list[-1] == "":  # Only prefix provided
            prefix = "/".join(prefix_record_list[:-1])
            record = None
        else:  # Prefix and record provided
            prefix = "/".join(prefix_record_list[:-1])
            record = prefix_record_list[-1]

        # Assign default prefix if the prefix is undefined or not in the list of
        # authorized ones.
        if prefix == "" or prefix not in settings.ID_PROVIDER_PREFIXES:
            return Response(
                {
                    "record": "/".join(prefix_record_list),
                    "url": request.build_absolute_uri("?"),
                    "message": "Invalid prefix specified",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if (
            record is not None
            and record != ""
            and re.match(r"^(%s|)$" % settings.PID_FORMAT, record) is None
        ):
            return Response(
                {
                    "record": "/".join(prefix_record_list),
                    "url": request.build_absolute_uri("?"),
                    "message": "Invalid record format",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        id_provider = self.provider_manager.get(provider)
        provider_response = id_provider.create(prefix, record)

        provider_content = json.loads(provider_response.content)
        return Response(provider_content, status=provider_response.status_code)

    def put(self, request, provider, record):
        """Update the value of a given handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        id_provider = self.provider_manager.get(provider)
        provider_response = id_provider.update(record)

        provider_content = json.loads(provider_response.content)

        return Response(provider_content, status=provider_response.status_code)

    def get(self, request, provider, record):
        """Retrieve the local data of a given handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        id_provider = self.provider_manager.get(provider)
        provider_response = id_provider.get(record)

        try:
            query_result = get_data_by_pid(
                json.loads(provider_response.content)["url"], request.user
            )
            return Response(
                DataSerializer(query_result).data, status=status.HTTP_200_OK
            )
        except DoesNotExist:
            content = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "No data with specified handle found",
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            content = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(ex),
            }
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, provider, record):
        """Delete a handle record

        Args:
            request:
            provider:
            record:

        Returns:
        """
        id_provider = self.provider_manager.get(provider)
        provider_response = id_provider.delete(record)

        provider_content = json.loads(provider_response.content)

        return Response(provider_content, status=provider_response.status_code)
