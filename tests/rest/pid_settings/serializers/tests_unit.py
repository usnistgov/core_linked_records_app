""" Unit tests for `core_linked_records.rest.pid_settings.serializers`.
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from core_linked_records_app.rest.pid_settings import (
    serializers as pid_settings_serializers,
)


class TestPidSettingsSerializerUpdate(TestCase):
    """Unit tests for `PidSettingsSerializer.update` method."""

    def setUp(self) -> None:
        """setUp"""
        self.context = {"request": MagicMock()}
        self.mock_kwargs = {
            "instance": Mock(),
            "validated_data": {"auto_set_pid": True},
        }

    @patch.object(pid_settings_serializers, "pid_settings_api")
    def test_pid_settings_system_api_upsert_called(
        self, mock_pid_settings_api
    ):
        """test_pid_settings_system_api_upsert_called"""
        serializer = pid_settings_serializers.PidSettingsSerializer()
        serializer._context = self.context
        serializer.update(**self.mock_kwargs)

        mock_pid_settings_api.upsert.assert_called_with(
            self.mock_kwargs["instance"], self.context["request"].user
        )

    @patch.object(pid_settings_serializers, "pid_settings_api")
    def test_succesful_execution_returns_pid_settings_system_api_upsert(
        self, mock_pid_settings_api
    ):
        """test_pid_settings_system_api_upsert_called"""
        expected_value = Mock()
        mock_pid_settings_api.upsert.return_value = expected_value
        serializer = pid_settings_serializers.PidSettingsSerializer()
        serializer._context = self.context

        self.assertEqual(serializer.update(**self.mock_kwargs), expected_value)
