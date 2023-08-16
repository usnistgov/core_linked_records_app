""" Unit tests for `core_linked_records_app.access_control.discover`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from core_linked_records_app.access_control import discover
from core_linked_records_app.access_control import rights
from core_main_app.permissions import rights as main_rights


class TestInitPermissions(TestCase):
    """Unit tests for `init_permission` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_default_group = MagicMock()
        self.mock_anonymous_group = MagicMock()

    @patch.object(discover, "logger")
    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_groups_retrieval_error_is_logged(
        self,
        mock_group_api,
        mock_permissions_api,  # noqa, pylint: disable=unused-argument
        mock_logger,
    ):
        """test_groups_retrieval_error_is_logged"""
        mock_group_api.get_or_create.side_effect = Exception(
            "mock_group_exception"
        )
        discover.init_permissions()
        mock_logger.error.assert_called()

    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_groups_are_retrieved(
        self,
        mock_group_api,
        mock_permissions_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_groups_are_retrieved"""
        mock_group_api.get_or_create.return_value = (MagicMock(), False)
        discover.init_permissions()
        mock_group_api.get_or_create.assert_has_calls(
            [
                call(name=main_rights.DEFAULT_GROUP),
            ]
        )

    @patch.object(discover, "logger")
    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_permissions_retrieval_error_is_logged(
        self,
        mock_group_api,  # noqa, pylint: disable=unused-argument
        mock_permissions_api,
        mock_logger,
    ):
        """test_permissions_retrieval_error_is_logged"""
        mock_permissions_api.get_by_codename.side_effect = Exception(
            "mock_get_by_codename_exception"
        )
        discover.init_permissions()
        mock_logger.error.assert_called()

    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_permissions_are_retrieved(
        self,
        mock_group_api,
        mock_permissions_api,
    ):
        """test_permissions_are_retrieved"""
        mock_group_api.get_or_create.return_value = (MagicMock(), False)
        discover.init_permissions()
        mock_permissions_api.get_by_codename.assert_has_calls(
            [
                call(codename=rights.CAN_READ_PID_SETTINGS),
            ]
        )

    @patch.object(discover, "logger")
    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_default_group_add_permissions_error_is_logged(
        self,
        mock_group_api,
        mock_permissions_api,  # noqa, pylint: disable=unused-argument
        mock_logger,
    ):
        """test_default_group_add_permissions_error_is_logged"""
        self.mock_default_group.permissions.add.side_effect = Exception(
            "mock_default_group_permission_add_exception"
        )
        mock_group_api.get_or_create.side_effect = [
            (self.mock_default_group, False),
        ]

        discover.init_permissions()
        mock_logger.error.assert_called()

    @patch.object(discover, "permissions_api")
    @patch.object(discover, "group_api")
    def test_default_group_has_all_permissions(
        self,
        mock_group_api,
        mock_permissions_api,
    ):
        """test_default_group_has_all_permissions"""
        mock_permission_object_list = ["can_read_pid_settings_perm"]

        mock_group_api.get_or_create.side_effect = [
            (self.mock_default_group, False),
            (self.mock_anonymous_group, False),
        ]
        mock_permissions_api.get_by_codename.side_effect = (
            mock_permission_object_list
        )

        discover.init_permissions()
        self.mock_default_group.permissions.add.assert_called_with(
            *mock_permission_object_list
        )
