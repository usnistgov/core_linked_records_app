""" Unit tests for admin views
"""
from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app.views.admin.views import PidSettingsView
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.mocks import MockRequest, MockTemplate, MockPidPath


class TestPidSettingsViewGet(TestCase):
    """Tests PidSettingsView get method"""

    def setUp(self) -> None:
        self.view = PidSettingsView()
        mock_user = create_mock_user(1, is_superuser=True)
        self.request = MockRequest()
        self.request.user = mock_user
        self.settings_json = {
            "path": "mock_path",
            "system_name": "mock_system_name",
            "prefixes": ["mock_prefix"],
        }

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_pid_path_api_get_all_called(
        self,
        mock_get_pid_path_api,
        mock_admin_render,
    ):
        """test_pid_path_api_get_all_called"""
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_get_pid_path_api.get_all.assert_called_with(self.request)

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_pid_path_get_all_failure_returns_error_page(
        self,
        mock_get_pid_path_api,
        mock_admin_render,
    ):
        """test_pid_path_get_all_failure_returns_error_page"""
        mock_get_pid_path_api.get_all.side_effect = Exception(
            "mock_get_pid_path_api_get_all_exception"
        )

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings_error.html",
            context={
                "error": "An error occured while retrieving the PID settings. "
                "Please contact an administrator for more information. Exception: "
                "mock_get_pid_path_api_get_all_exception."
            },
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.get_pid_settings_dict")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_get_pid_settings_dict_called(
        self,
        mock_get_pid_path_api,
        mock_get_pid_settings_dict,
        mock_admin_render,
    ):
        """test_get_pid_settings_dictcalled"""
        mock_get_pid_path_api.get_all.return_value = []
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_get_pid_settings_dict.assert_called()

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.get_pid_settings_dict")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_get_pid_settings_dict_failure_returns_error_page(
        self,
        mock_get_pid_path_api,
        mock_get_pid_settings_dict,
        mock_admin_render,
    ):
        """test_get_pid_settings_dict_failure_returns_error_page"""
        mock_get_pid_path_api.get_all.return_value = []
        mock_get_pid_settings_dict.side_effect = Exception(
            "mock_get_pid_settings_dict_exception"
        )
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings_error.html",
            context={
                "error": "An error occured while retrieving the PID settings. "
                "Please contact an administrator for more information. Exception: "
                "mock_get_pid_settings_dict_exception."
            },
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.get_pid_settings_dict")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_return_settings_page(
        self,
        mock_get_pid_path_api,
        mock_get_pid_settings_dict,
        mock_admin_render,
    ):
        """test_return_settings_page"""
        mock_get_pid_path_api.get_all.return_value = []
        mock_get_pid_settings_dict.return_value = self.settings_json
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings.html",
            assets={
                "js": [
                    {
                        "path": "core_linked_records_app/admin/js/pid_settings/auto_set_pid.js",
                        "is_raw": False,
                    }
                ],
                "css": [
                    "core_linked_records_app/admin/css/pid_settings.css",
                ],
            },
            context={"pid_settings": self.settings_json},
        )

    @patch("core_linked_records_app.views.admin.views.admin_render")
    @patch("core_linked_records_app.views.admin.views.get_pid_settings_dict")
    @patch("core_linked_records_app.views.admin.views.pid_path_api")
    def test_return_settings_page_with_pid_path(
        self,
        mock_get_pid_path_api,
        mock_get_pid_settings_dict,
        mock_admin_render,
    ):
        """test_return_settings_page_with_pid_path"""
        mock_pid_path1 = MockPidPath()
        mock_pid_path1.id = 1
        mock_pid_path1.path = "root.elem1"
        mock_pid_path1.template = MockTemplate(display_name="Template01")

        mock_pid_path2 = MockPidPath()
        mock_pid_path2.id = 2
        mock_pid_path2.path = "root.elem2"
        mock_pid_path2.template = MockTemplate(display_name="Template02")

        mock_get_pid_path_api.get_all.return_value = [
            mock_pid_path1,
            mock_pid_path2,
        ]
        mock_get_pid_settings_dict.return_value = self.settings_json
        mock_admin_render.return_value = None

        self.view.get(self.request)
        mock_admin_render.assert_called_with(
            self.request,
            "core_linked_records_app/admin/pid_settings.html",
            assets={
                "js": [
                    {
                        "path": "core_linked_records_app/admin/js/pid_settings/auto_set_pid.js",
                        "is_raw": False,
                    }
                ],
                "css": [
                    "core_linked_records_app/admin/css/pid_settings.css",
                ],
            },
            context={"pid_settings": self.settings_json},
        )
