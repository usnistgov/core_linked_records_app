""" Permission tests for core_linked_records_app.rest.pid_settings.views
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from rest_framework import status

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
)
from core_linked_records_app.rest.pid_settings import (
    views as pid_settings_views,
)
from core_linked_records_app.rest.pid_settings.serializers import (
    PidSettingsSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests import mocks


class TestPidSettingsViewGet(TestCase):
    """Test Pid Settings View Get"""

    @patch.object(PidSettingsSerializer, "__new__")
    @patch.object(pid_settings_api, "get")
    def test_anonymous_returns_403(
        self, mock_pid_settings_get, mock_pid_setting_settings_serializer
    ):
        """test_anonymous_returns_403"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_pid_setting_settings_serializer.return_value = Mock(data={})

        response = RequestMock.do_request_get(
            pid_settings_views.PidSettingsView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PidSettingsSerializer, "__new__")
    @patch.object(pid_settings_api, "get")
    def test_authenticated_returns_200(
        self, mock_pid_settings_get, mock_pid_setting_settings_serializer
    ):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_pid_setting_settings_serializer.return_value = Mock(data={})

        response = RequestMock.do_request_get(
            pid_settings_views.PidSettingsView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(PidSettingsSerializer, "__new__")
    @patch.object(pid_settings_api, "get")
    def test_staff_returns_200(
        self, mock_pid_settings_get, mock_pid_setting_settings_serializer
    ):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_pid_setting_settings_serializer.return_value = Mock(data={})

        response = RequestMock.do_request_get(
            pid_settings_views.PidSettingsView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidSettingsViewPatch(TestCase):
    """Test Pid Settings View Patch"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_patch(
            pid_settings_views.PidSettingsView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_403(self):
        """test_authenticated_returns_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            pid_settings_views.PidSettingsView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_403(self):
        """test_staff_returns_403"""

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            pid_settings_views.PidSettingsView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(pid_settings_api, "get")
    @patch.object(PidSettingsSerializer, "__new__")
    def test_superuser_returns_200(
        self, mock_pid_serializer, mock_pid_settings_get
    ):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_superuser=True)

        mock_pid_serializer.return_value = mocks.MockSerializer()
        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        response = RequestMock.do_request_patch(
            pid_settings_views.PidSettingsView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
