""" ACL tests for `core_linked_records.components.data.api`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.data import (
    api as pid_data_api,
    access_control as pid_data_acl,
)
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_main_app.access_control import api as main_acl
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.data import api as main_data_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestGetDataByPid(TestCase):
    """ACL tests for `get_data_by_pid` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_query_result = MagicMock()

    def setup_mocks(
        self, mock_get_all, mock_execute_json_query, user, owner=None
    ) -> None:
        """setup_mocks"""
        self.mock_request.user = user
        self.mock_query_result.user_id = owner.id if owner else user.id

        mock_get_all.return_value = []
        mock_execute_json_query.return_value = [self.mock_query_result]

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_superuser_can_access(self, mock_get_all, mock_execute_json_query):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        self.setup_mocks(mock_get_all, mock_execute_json_query, user)

        self.assertEqual(
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request),
            self.mock_query_result,
        )

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_cannot_access_private(
        self,
        mock_setting,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_all,
        mock_execute_json_query,
    ):
        """test_registered_user_not_owner_cannot_access_private"""
        mock_setting.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")
        owner = create_mock_user("2")

        self.setup_mocks(mock_get_all, mock_execute_json_query, user, owner)

        with self.assertRaises(AccessControlError):
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_can_access_public(
        self,
        mock_settings,
        mock_workspace_api,
        mock_get_all,
        mock_execute_json_query,
    ):
        """test_registered_user_not_owner_can_access_public"""
        mock_public_workspace = MagicMock()
        self.mock_query_result.workspace = mock_public_workspace
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1")
        owner = create_mock_user("2")

        self.setup_mocks(mock_get_all, mock_execute_json_query, user, owner)

        self.assertEqual(
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request),
            self.mock_query_result,
        )

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_and_owner_can_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_all,
        mock_execute_json_query,
    ):
        """test_registered_user_and_owner_can_access_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")

        self.setup_mocks(mock_get_all, mock_execute_json_query, user)

        self.assertEqual(
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request),
            self.mock_query_result,
        )

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_not_public_cannot_access(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_all,
        mock_execute_json_query,
    ):
        """test_anonymous_user_not_public_cannot_access"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(mock_get_all, mock_execute_json_query, user)

        with self.assertRaises(AccessControlError):
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_and_public_can_access(
        self,
        mock_settings,
        mock_workspace_api,
        mock_get_all,
        mock_execute_json_query,
    ):
        """test_anonymous_user_and_public_can_access"""
        mock_public_workspace = MagicMock()
        self.mock_query_result.workspace = mock_public_workspace
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(mock_get_all, mock_execute_json_query, user)

        self.assertEqual(
            pid_data_api.get_data_by_pid("mock_pid", self.mock_request),
            self.mock_query_result,
        )


class TestGetPidForData(TestCase):
    """ACL tests for `get_pid_for_data` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_request = MagicMock()
        self.mock_data = MagicMock()

        self.mock_data_pid = "mock_data_pid"

    def setup_mocks(
        self,
        mock_data,
        mock_get_by_id,
        mock_get_value_from_dot_notation,
        user,
        owner=None,
    ) -> None:
        """setup_mocks"""
        self.mock_request.user = user
        self.mock_data.user_id = owner.id if owner else user.id

        mock_data.get_by_id.return_value = self.mock_data
        mock_get_by_id.return_value = self.mock_data

        mock_get_value_from_dot_notation.return_value = self.mock_data_pid

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    def test_superuser_can_access(
        self,
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request),
            self.mock_data_pid,
        )

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_cannot_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_registered_user_not_owner_cannot_access_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False

        owner = create_mock_user("1")
        user = create_mock_user("2")

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
            owner,
        )

        with self.assertRaises(AccessControlError):
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_can_access_public(
        self,
        mock_settings,
        mock_workspace_api,
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_registered_user_not_owner_can_access_public"""
        mock_public_workspace = MagicMock()
        self.mock_data.workspace = mock_public_workspace
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1")
        owner = create_mock_user("2")

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
            owner,
        )

        self.assertEqual(
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request),
            self.mock_data_pid,
        )

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_and_owner_can_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_registered_user_and_owner_can_access_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request),
            self.mock_data_pid,
        )

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_not_public_cannot_access(
        self,
        mock_settings,
        mock_workspace_api,
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_anonymous_user_not_public_cannot_access"""
        mock_public_workspace = MagicMock()
        self.mock_data.workspace = mock_public_workspace
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
        )

        with self.assertRaises(AccessControlError):
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_and_public_can_access(
        self,
        mock_settings,
        mock_workspace_api,
        mock_data,
        mock_get_by_id,
        mock_get_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,  # noqa, pylint: disable=unused-argument
        mock_is_valid_pid_value,  # noqa, pylint: disable=unused-argument
    ):
        """test_anonymous_user_and_public_can_access"""
        mock_public_workspace = MagicMock()
        self.mock_data.workspace = mock_public_workspace
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_data,
            mock_get_by_id,
            mock_get_value_from_dot_notation,
            user,
        )

        self.assertEqual(
            pid_data_api.get_pid_for_data("mock_data_id", self.mock_request),
            self.mock_data_pid,
        )
