""" Data Xml renderer for django REST API
"""
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


class DataXmlRenderer(renderers.BaseRenderer):
    """Data Xml Renderer"""

    media_type = "application/xml"
    format = "xml"
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        """Render the data object by just returning the xml_content field

        Args:
            data:
            media_type:
            renderer_context:

        Returns: xml string
        """

        # check errors
        if "status" in data and data["status"] == "error":
            if data["code"] == HTTP_404_NOT_FOUND:
                return HttpResponse(status=HTTP_404_NOT_FOUND)

            return HttpResponse(status=HTTP_500_INTERNAL_SERVER_ERROR)

        return data["xml_content"]
