""" ACL tests for `core_linked_records.components.pid_path.api`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.pid_path import (
    api as pid_path_api,
    models as pid_path_models,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template import (
    access_control as template_access_control,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestGetByTemplate(TestCase):
    """ACL tests for `get_by_template` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_template = MagicMock()
        self.mock_pid_path = MagicMock()

    def setup_mocks(self, owner) -> None:
        """setup_mocks"""
        self.mock_template.user = owner.id if owner else None

    @patch.object(pid_path_models.PidPath, "get_by_template")
    def test_superuser_can_access(self, mock_get_by_template):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(user)

        self.assertEqual(
            pid_path_api.get_by_template(self.mock_template, user),
            self.mock_pid_path,
        )

    @patch.object(pid_path_models.PidPath, "get_by_template")
    def test_registered_user_not_owner_cannot_access_private(
        self, mock_get_by_template
    ):
        """test_registered_user_without_perm_cannot_access"""
        user = create_mock_user("1")
        owner = create_mock_user("2")

        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(owner)

        with self.assertRaises(AccessControlError):
            pid_path_api.get_by_template(self.mock_template, user)

    @patch.object(pid_path_models.PidPath, "get_by_template")
    def test_registered_user_not_owner_can_access_public(
        self, mock_get_by_template
    ):
        """test_registered_user_without_perm_cannot_access"""
        user = create_mock_user("1")

        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(None)  # noqa

        self.assertEqual(
            pid_path_api.get_by_template(self.mock_template, user),
            self.mock_pid_path,
        )

    @patch.object(pid_path_models.PidPath, "get_by_template")
    def test_registered_user_and_owner_can_access_private(
        self, mock_get_by_template
    ):
        """test_registered_user_with_perm_can_access"""
        user = create_mock_user("1")

        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(user)

        self.assertEqual(
            pid_path_api.get_by_template(self.mock_template, user),
            self.mock_pid_path,
        )

    @patch.object(pid_path_models.PidPath, "get_by_template")
    @patch.object(template_access_control, "settings")
    def test_anonymous_user_cannot_access_private(
        self, mock_settings, mock_get_by_template
    ):
        """test_anonymous_user_without_perm_cannot_access"""
        user = create_mock_user("1", is_anonymous=True)

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(None)  # noqa

        with self.assertRaises(AccessControlError):
            pid_path_api.get_by_template(self.mock_template, user)

    @patch.object(pid_path_models.PidPath, "get_by_template")
    @patch.object(template_access_control, "settings")
    def test_anonymous_user_can_access_public(
        self, mock_settings, mock_get_by_template
    ):
        """test_anonymous_user_with_perm_can_access"""
        user = create_mock_user("1", is_anonymous=True)

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_get_by_template.return_value = self.mock_pid_path
        self.setup_mocks(None)  # noqa

        self.assertEqual(
            pid_path_api.get_by_template(self.mock_template, user),
            self.mock_pid_path,
        )
