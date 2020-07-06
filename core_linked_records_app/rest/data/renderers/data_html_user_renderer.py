""" Data HTML renderer for django REST API
"""
import logging

from django.http import HttpResponse
from rest_framework import renderers, status
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render

LOGGER = logging.getLogger(__name__)


class DataHtmlUserRenderer(renderers.BaseRenderer):
    # FIXME class is very close to ViewData, remove duplicated code.
    media_type = "text/html"
    format = "html"
    charset = "utf-8"

    @staticmethod
    def build_page(data, request):
        context = {
            "data": data_api.get_by_id(data["id"], request.user),
            "share_pid_button": True,
        }

        assets = {
            "js": [
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {"path": "core_main_app/user/js/data/detail.js", "is_raw": False},
                {"path": "core_main_app/user/js/sharing_modal.js", "is_raw": False,},
                {
                    "path": "core_linked_records_app/user/js/sharing/data_detail.js",
                    "is_raw": False,
                },
            ],
            "css": ["core_main_app/common/css/XMLTree.css"],
        }
        modals = ["core_linked_records_app/user/sharing/data_detail/modal.html"]

        # check errors
        if "status" in data and data["status"] == "error":
            if data["code"] == HTTP_404_NOT_FOUND:
                return HttpResponse(status=HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return render(
                request,
                "core_main_app/user/data/detail.html",
                context=context,
                assets=assets,
                modals=modals,
            )

    def render(self, data, media_type=None, renderer_context=None):
        """ Render the data object by returning the user template

        Args:
            data:
            media_type:
            renderer_context:

        Returns: html page
        """

        try:
            request = (
                renderer_context["request"] if "request" in renderer_context else None
            )
            # check the renderer format
            if (
                request
                and request.query_params != {}
                and "format" in request.query_params
                and request.query_params["format"] != "html"
            ):
                raise APIException(
                    "Wrong data format parameter.", status.HTTP_404_NOT_FOUND
                )

            return self.build_page(data, renderer_context["request"])
        except APIException as api_error:
            return render(
                renderer_context["request"],
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
                renderer_context["request"],
                "core_main_app/common/commons/error.html",
                context={"error": error_msg},
            )
