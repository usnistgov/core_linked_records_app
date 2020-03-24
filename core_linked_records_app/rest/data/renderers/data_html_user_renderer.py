""" Data HTML renderer for django REST API
"""
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from core_main_app.components.data import api as data_api
from core_main_app.utils.rendering import render


class DataHtmlUserRenderer(renderers.BaseRenderer):
    media_type = 'text/html'
    format = 'html'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """ Render the data object by returning the user template

        Args:
            data:
            media_type:
            renderer_context:

        Returns: html page
        """
        context = {
            'data': data_api.get_by_id(data["id"], renderer_context["request"].user)
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
                renderer_context['request'],
                'core_main_app/user/data/detail.html', context=context,
                assets=assets
            )
