""" Unit tests for data_html_user_renderer packages.
"""
from unittest import TestCase
from unittest.mock import Mock, patch

from rest_framework import status

from core_linked_records_app.rest.data.renderers import data_html_user_renderer
from tests.mocks import MockResponse


class TestDataHtmlUserRendererRender(TestCase):
    """Unit tests for `DataHtmlUserRenderer.render` method."""

    @patch.object(data_html_user_renderer, "render")
    def test_http_403_response_renders_error_page(self, mock_render):
        """test_http_403_response_renders_error_page"""
        mock_data = Mock()
        mock_response = MockResponse()
        mock_response.status_code = status.HTTP_403_FORBIDDEN
        mock_renderer_context = {
            "response": mock_response,
            "kwargs": {"record": "mock_record"},
        }

        renderer = data_html_user_renderer.DataHtmlUserRenderer()
        renderer.render(mock_data, renderer_context=mock_renderer_context)

        mock_render.assert_called_with(
            None,
            "core_main_app/common/commons/error.html",
            context={
                "error": "The user doesn't have enough rights to access "
                "document mock_record"
            },
        )
