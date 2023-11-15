""" ACL tests for `core_linked_records.components.oai_record.api`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.components.oai_record import api as oai_record_api
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_main_app.access_control import api as main_acl_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_oaipmh_harvester_app.components.oai_record import (
    api as oaipmh_harvester_oai_record_api,
)


class TestGetPidForData(TestCase):
    """ACL tests for `get_pid_for_data` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_get_value_from_dot_notation_return_value = (
            "mock_get_value_from_dot_notation"
        )

    def setup_mocks(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        user,
    ) -> None:
        """setup_mocks"""
        self.mock_request.user = user

        mock_get_by_id.return_value = MagicMock()
        mock_get_by_template.return_value = MagicMock()
        mock_get_value_from_dot_notation.return_value = (
            self.mock_get_value_from_dot_notation_return_value
        )

    @patch.object(oai_record_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(oaipmh_harvester_oai_record_api, "get_by_id")
    def test_superuser_can_access(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
    ):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        self.setup_mocks(
            mock_get_by_id,
            mock_get_by_template,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            oai_record_api.get_pid_for_data(
                "mock_oai_record_id", self.mock_request
            ),
            self.mock_get_value_from_dot_notation_return_value,
        )

    @patch.object(oai_record_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(oaipmh_harvester_oai_record_api, "get_by_id")
    def test_registered_user_can_access(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
    ):
        """test_registered_user_can_access"""
        user = create_mock_user("1")

        self.setup_mocks(
            mock_get_by_id,
            mock_get_by_template,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            oai_record_api.get_pid_for_data(
                "mock_oai_record_id", self.mock_request
            ),
            self.mock_get_value_from_dot_notation_return_value,
        )

    @patch.object(oai_record_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(oaipmh_harvester_oai_record_api, "get_by_id")
    @patch.object(main_acl_api, "settings")
    def test_anonymous_user_not_public_cannot_access(
        self,
        mock_settings,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
    ):
        """test_anonymous_user_not_public_cannot_access"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_get_by_id,
            mock_get_by_template,
            mock_get_value_from_dot_notation,
            user,
        )

        with self.assertRaises(AccessControlError):
            oai_record_api.get_pid_for_data(
                "mock_oai_record_id", self.mock_request
            )

    @patch.object(oai_record_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(oaipmh_harvester_oai_record_api, "get_by_id")
    @patch.object(main_acl_api, "settings")
    def test_anonymous_user_and_public_can_access(
        self,
        mock_settings,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
    ):
        """test_anonymous_user_and_public_can_access"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_get_by_id,
            mock_get_by_template,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            oai_record_api.get_pid_for_data(
                "mock_oai_record_id", self.mock_request
            ),
            self.mock_get_value_from_dot_notation_return_value,
        )
