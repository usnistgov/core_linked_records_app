""" Unit tests for data_html_renderer packages.
"""

from unittest import TestCase

from rest_framework import status

from core_linked_records_app.rest.pid.views import DataHtmlRenderByPID
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDataHtmlRenderByPID(TestCase):
    """TestDataHtmlRenderByPID"""

    def test_get_data_html_render_by_pid_returns_http_400_response_when_pid_is_missing(
        self,
    ):
        """test_get_data_html_render_by_pid_returns_http_400_response_when_pid_is_missing"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            DataHtmlRenderByPID.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
