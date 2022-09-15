""" Unit tests for core_linked_records_app.rest.pid_settings.views
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.rest.pid_settings import views as pid_settings_views
from core_linked_records_app.rest.pid_settings.serializers import (
    PidSettingsSerializer,
)
from tests import mocks


class TestPidSettingsViewGet(TestCase):
    """Test Pid Settings View Get"""

    def setUp(self):
        """setUp"""

        self.mock_request = mocks.MockRequest()

    @patch.object(pid_settings_api, "get")
    def test_pid_settings_api_get_fails_returns_500(self, mock_pid_settings_get):
        """test_pid_settings_api_get_fails_returns_500"""

        mock_pid_settings_get.side_effect = Exception("mock_pid_settings_get_exception")

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(PidSettingsSerializer, "__new__")
    @patch.object(pid_settings_api, "get")
    def test_pid_settings_serializer_fails_returns_500(
        self, mock_pid_settings_get, mock_pid_settings_serializer
    ):
        """test_pid_settings_serializer_fails_returns_500"""

        mock_pid_settings_get.return_value = "mock_pid_settings"
        mock_pid_settings_serializer.side_effect = Exception(
            "mock_pid_settings_serializer_exception"
        )

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(PidSettingsSerializer, "__new__")
    @patch.object(pid_settings_api, "get")
    def test_success_returns_200(
        self, mock_pid_settings_get, mock_pid_settings_serializer
    ):
        """test_success_returns_200"""

        mock_pid_settings_get.return_value = "mock_pid_settings"
        mock_pid_settings_serializer.return_value = mocks.MockSerializer()

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 200)


class TestPidSettingsViewPatch(TestCase):
    """Test Pid Settings View Patch"""

    def setUp(self):
        """setUp"""

        self.mock_request = mocks.MockRequest()
        self.mock_request.user = create_mock_user("1", is_superuser=True)

    @patch.object(PidSettingsSerializer, "__new__")
    def test_pid_serializer_init_fails_returns_500(self, mock_pid_settings_serializer):
        """test_pid_serializer_init_fails_returns_500"""

        mock_pid_settings_serializer.side_effect = Exception(
            "mock_pid_settings_serializer_exception"
        )

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(PidSettingsSerializer, "__new__")
    def test_pid_serializer_is_valid_fails_returns_500(
        self, mock_pid_settings_serializer
    ):
        """test_pid_serializer_is_valid_fails_returns_500"""

        mock_pid_settings_serializer.return_value = mocks.MockSerializer(
            is_valid_exc=Exception("mock_pid_settings_serializer_is_valid_exc")
        )

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(PidSettingsSerializer, "__new__")
    def test_pid_serializer_not_valid_returns_400(self, mock_pid_settings_serializer):
        """test_pid_serializer_not_valid_returns_400"""

        mock_pid_settings_serializer.return_value = mocks.MockSerializer(
            is_valid_result=False
        )

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 400)

    @patch.object(PidSettingsSerializer, "__new__")
    def test_pid_serializer_update_fails_returns_500(
        self, mock_pid_settings_serializer
    ):
        """test_pid_serializer_update_fails_returns_500"""

        mock_pid_settings_serializer.return_value = mocks.MockSerializer(
            is_valid_result=True,
            update_exc=Exception("mock_pid_settings_serializer_update_exception"),
        )

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_settings_views.PidSettingsView, "get")
    @patch.object(PidSettingsSerializer, "__new__")
    def test_get_fails_returns_500(self, mock_pid_settings_serializer, mock_view_get):
        """test_get_fails_returns_500"""

        mock_pid_settings_serializer.return_value = mocks.MockSerializer(
            is_valid_result=True
        )
        mock_view_get.side_effect = Exception("mock_view_get_exception")

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_settings_views.PidSettingsView, "get")
    @patch.object(PidSettingsSerializer, "__new__")
    def test_success_returns_200(self, mock_pid_settings_serializer, mock_view_get):
        """test_success_returns_200"""

        mock_pid_settings_serializer.return_value = mocks.MockSerializer(
            is_valid_result=True
        )
        mock_view_get.return_value = mocks.MockResponse()

        test_view = pid_settings_views.PidSettingsView()
        response = test_view.patch(self.mock_request)

        self.assertEqual(response.status_code, 200)
