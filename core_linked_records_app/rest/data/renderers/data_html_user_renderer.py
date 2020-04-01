""" Data HTML renderer for django REST API
"""
import logging
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render

LOGGER = logging.getLogger(__name__)


class DataHtmlUserRenderer(renderers.BaseRenderer):
    media_type = 'text/html'
    format = 'html'
    charset = 'utf-8'

    @staticmethod
    def build_page(data, request):
        context = {
            'data': data_api.get_by_id(data["id"], request.user)
        }

        assets = {
            "js": [
                {
                    "path": 'core_main_app/common/js/XMLTree.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/data/detail.js',
                    "is_raw": False
                },
            ],
            "css": ["core_main_app/common/css/XMLTree.css"],
        }

        # check errors
        if 'status' in data and data['status'] == 'error':
            if data['code'] == HTTP_404_NOT_FOUND:
                return HttpResponse(status=HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return render(
                request, 'core_main_app/user/data/detail.html', context=context,
                assets=assets
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
            return self.build_page(data, renderer_context["request"])
        except Exception as e:
            LOGGER.error("Error while building data page: %s" % str(e))

            if "kwargs" in renderer_context and "record" in renderer_context["kwargs"]:
                error_msg = "Document %s does not exist." % \
                            renderer_context["kwargs"]["record"]
            else:
                error_msg = "Invalid request provided."

            return render(
                renderer_context["request"], 'core_main_app/common/commons/error.html',
                context={
                    "error": error_msg
                }
            )
