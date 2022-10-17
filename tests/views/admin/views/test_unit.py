""" Unit tests for admin views
"""
from unittest import TestCase
from unittest.mock import patch
from urllib.parse import urljoin

from django.urls import reverse
from rest_framework import status

from core_linked_records_app.views.admin.views import PidSettingsView
from tests.mocks import MockResponse, MockRequest, MockTemplate
from tests.test_settings import SERVER_URI


class TestPidSettingsViewGet(TestCase):
    """Tests PidSettingsView get method"""

    def setUp(self) -> None:
        self.view = PidSettingsView()
        self.request = MockRequest()
        self.settings_json = {
            "xpath": "mock_xpath",
            "system_name": "mock_system_name",
            "prefixes": ["mock_prefix"],
        }

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_pid_settings_rest_called(
        self, mock_send_get_request, mock_admin_render
    ):
        """test_pid_settings_rest_called"""
        mock_send_get_request.side_effect = [
            MockResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
            MockResponse(json_data=[]),
        ]
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_send_get_request.assert_called_with(
            urljoin(SERVER_URI, reverse("core_linked_records_app_settings")),
            cookies={"sessionid": self.request.session.session_key},
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_pid_settings_rest_failure_returns_error_page(
        self, mock_send_get_request, mock_admin_render
    ):
        """test_pid_settings_rest_failure_returns_error_page"""
        mock_send_get_request.side_effect = [
            MockResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
            MockResponse(json_data=[]),
        ]
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings_error.html",
            context={
                "error": "An error occured while retrieving the PID settings. "
                "Please contact an administrator for more information."
            },
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_pid_xpath_rest_called(
        self, mock_send_get_request, mock_admin_render
    ):
        """test_pid_xpath_rest_called"""
        mock_send_get_request.side_effect = [
            MockResponse(json_data=self.settings_json),
            MockResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
        ]
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_send_get_request.assert_called_with(
            urljoin(
                SERVER_URI,
                reverse("core_linked_records_app_settings_xpath_list"),
            ),
            cookies={"sessionid": self.request.session.session_key},
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_pid_xpath_rest_failure_returns_error_page(
        self, mock_send_get_request, mock_admin_render
    ):
        """test_pid_xpath_rest_failure_returns_error_page"""
        mock_send_get_request.side_effect = [
            MockResponse(json_data=self.settings_json),
            MockResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR),
        ]

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings_error.html",
            context={
                "error": "An error occured while retrieving the list of PID XPath. "
                "Please contact an administrator for more information."
            },
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_return_settings_page(
        self, mock_send_get_request, mock_admin_render
    ):
        """test_return_settings_page"""
        mock_send_get_request.side_effect = [
            MockResponse(json_data=self.settings_json),
            MockResponse(json_data=[]),
        ]
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings.html",
            assets={
                "js": [
                    {
                        "path": "core_linked_records_app/admin/js/pid_settings/auto_set_pid.js",
                        "is_raw": True,
                    }
                ],
                "css": [
                    "core_linked_records_app/admin/css/pid_settings.css",
                ],
            },
            context={"pid_settings": self.settings_json},
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch("core_linked_records_app.views.admin.views.send_get_request")
    def test_return_settings_page_with_xpath(
        self,
        mock_send_get_request,
        mock_template_api_get_by_id,
        mock_admin_render,
    ):
        """test_return_settings_page_with_xpath"""
        mock_send_get_request.side_effect = [
            MockResponse(json_data=self.settings_json),
            MockResponse(
                json_data=[
                    {"id": 1, "xpath": "root.elem1", "template": 1},
                    {"id": 1, "xpath": "root.elem2", "template": 2},
                ]
            ),
        ]
        mock_template_api_get_by_id.side_effect = [
            MockTemplate(display_name="Template01"),
            MockTemplate(display_name="Template02"),
        ]
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings.html",
            assets={
                "js": [
                    {
                        "path": "core_linked_records_app/admin/js/pid_settings/auto_set_pid.js",
                        "is_raw": True,
                    }
                ],
                "css": [
                    "core_linked_records_app/admin/css/pid_settings.css",
                ],
            },
            context={"pid_settings": self.settings_json},
        )
