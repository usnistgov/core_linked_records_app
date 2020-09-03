""" Data HTML renderer for django REST API
"""
import logging

from django.http import HttpResponse
from rest_framework import renderers, status
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render
from core_main_app.utils.view_builders import data as data_view_builder

LOGGER = logging.getLogger(__name__)


class DataHtmlUserRenderer(renderers.BaseRenderer):
    media_type = "text/html"
    format = "html"
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        """Render the data object by returning the user template

        Args:
            data:
            media_type:
            renderer_context:

        Returns: html page
        """
        # If the data retrieved contains an error
        if "status" in data and data["status"] == "error":
            if data["code"] == HTTP_404_NOT_FOUND:
                return HttpResponse(status=HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=HTTP_500_INTERNAL_SERVER_ERROR)

        # Build the request object or set it up to None if undefined
        request = renderer_context["request"] if "request" in renderer_context else None

        try:
            # Check the renderer format
            if (
                request
                and request.query_params != {}
                and "format" in request.query_params
                and request.query_params["format"] != "html"
            ):
                raise APIException(
                    "Wrong data format parameter.", status.HTTP_404_NOT_FOUND
                )

            data_object = data_api.get_by_id(data["id"], request.user)
            page_context = data_view_builder.build_page(data_object)

            return data_view_builder.render_page(request, render, page_context)
        except APIException as api_error:
            return render(
                request,
                "core_main_app/common/commons/error.html",
                context={"error": str(api_error)},
            )
        except Exception as e:
            LOGGER.error("Error while building data page: %s" % str(e))

            if "kwargs" in renderer_context and "record" in renderer_context["kwargs"]:
                error_msg = (
                    "Document %s does not exist." % renderer_context["kwargs"]["record"]
                )
            else:
                error_msg = "Invalid request provided."

            return render(
                request,
                "core_main_app/common/commons/error.html",
                context={"error": error_msg},
            )
