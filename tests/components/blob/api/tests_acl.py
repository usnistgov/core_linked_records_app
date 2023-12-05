""" ACL tests for `core_linked_records.components.blob.api`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.blob import (
    api as blob_api,
    access_control as blob_acl,
)
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.system.local_id import api as local_id_system_api
from core_main_app.access_control import api as main_acl
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests import mocks


class TestGetBlobByPid(TestCase):
    """ACL tests for `get_blob_by_pid` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob = mocks.MockDocument()

    def setup_mocks(
        self,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
        user,
        owner=None,
    ) -> None:
        """setup_mocks"""
        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.return_value = None

        self.mock_blob.user_id = owner.id if owner else user.id
        mock_blob_module = mocks.MockModule()
        mock_blob_module.get_by_id_return_value = self.mock_blob
        mock_getattr.return_value = mock_blob_module

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    def test_superuser_can_access(
        self,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)
        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user
        )

        self.assertEqual(
            blob_api.get_blob_by_pid("mock_pid", user), self.mock_blob
        )

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_cannot_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_registered_user_not_owner_cannot_access_private"""

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")
        owner = create_mock_user("2")
        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user, owner
        )

        with self.assertRaises(AccessControlError):
            blob_api.get_blob_by_pid("mock_pid", user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_can_access_public(
        self,
        mock_settings,
        mock_workspace_api,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_registered_user_not_owner_can_access_public"""
        mock_public_workspace = MagicMock()
        self.mock_blob.workspace = mock_public_workspace

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1")
        owner = create_mock_user("2")
        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user, owner
        )

        self.assertEqual(
            blob_api.get_blob_by_pid("mock_pid", user), self.mock_blob
        )

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_and_owner_can_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_registered_user_and_owner_can_access_private"""

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")
        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user
        )

        self.assertEqual(
            blob_api.get_blob_by_pid("mock_pid", user), self.mock_blob
        )

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_not_publc_cannot_access(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_anonymous_user_not_publc_cannot_access"""

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False

        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user
        )

        with self.assertRaises(AccessControlError):
            blob_api.get_blob_by_pid("mock_pid", user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_and_public_can_access(
        self,
        mock_settings,
        mock_workspace_api,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_anonymous_user_and_public_can_access"""
        mock_public_workspace = MagicMock()
        self.mock_blob.workspace = mock_public_workspace

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]

        user = create_mock_user("1", is_anonymous=True)
        self.setup_mocks(
            mock_get_by_name, mock_import_module, mock_getattr, user
        )

        self.assertEqual(
            blob_api.get_blob_by_pid("mock_pid", user), self.mock_blob
        )


class TestGetPidForBlob(TestCase):
    """ACL tests for `get_pid_for_blob` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob = MagicMock()
        self.mock_blob_pid = "mock_blob_pid"

    def setup_mocks(
        self,
        mock_blob_model,
        mock_blob_system_api,
        user,
        owner=None,
    ) -> None:
        """setup_mocks"""
        self.mock_blob.user_id = owner.id if owner else user.id
        mock_blob_model.get_by_id.return_value = self.mock_blob
        mock_blob_system_api.get_pid_for_blob.return_value = self.mock_blob_pid

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    def test_superuser_can_access(
        self,
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        self.setup_mocks(mock_blob_model, mock_blob_system_api, user)
        self.assertEqual(
            blob_api.get_pid_for_blob("mock_blob_id", user), self.mock_blob_pid
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_cannot_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_registered_user_not_owner_cannot_access_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1", has_perm=False)
        owner = create_mock_user("2")

        self.setup_mocks(mock_blob_model, mock_blob_system_api, user, owner)
        with self.assertRaises(AccessControlError):
            blob_api.get_pid_for_blob("mock_blob_id", user)

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_not_owner_can_access_public(
        self,
        mock_settings,
        mock_workspace_api,
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_registered_user_not_owner_can_access_public"""
        mock_public_workspace = MagicMock()
        self.mock_blob.workspace = mock_public_workspace

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1")
        owner = create_mock_user("2")

        self.setup_mocks(
            mock_blob_model,
            mock_blob_system_api,
            user,
            owner,
        )
        self.assertEqual(
            blob_api.get_pid_for_blob("mock_blob_id", user), self.mock_blob_pid
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_registered_user_and_owner_can_access_private(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_registered_user_and_owner_can_access_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1")

        self.setup_mocks(mock_blob_model, mock_blob_system_api, user)
        self.assertEqual(
            blob_api.get_pid_for_blob("mock_blob_id", user), self.mock_blob_pid
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_not_public_cannot_access(
        self,
        mock_settings,
        mock_workspace_api,  # noqa, pylint: disable=unused-argument
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_anonymous_user_not_public_cannot_access"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(mock_blob_model, mock_blob_system_api, user)

        with self.assertRaises(AccessControlError):
            blob_api.get_pid_for_blob("mock_blob_id", user)

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    @patch.object(main_acl, "settings")
    def test_anonymous_user_and_public_can_access(
        self,
        mock_settings,
        mock_workspace_api,
        mock_blob_model,
        mock_blob_system_api,
    ):
        """test_anonymous_user_and_public_can_access"""
        mock_public_workspace = MagicMock()
        self.mock_blob.workspace = mock_public_workspace

        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = [
            mock_public_workspace
        ]
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(mock_blob_model, mock_blob_system_api, user)
        self.assertEqual(
            blob_api.get_pid_for_blob("mock_blob_id", user), self.mock_blob_pid
        )


class TestSetPidForBlob(TestCase):
    """ACL tests for `set_pid_for_blob` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob_pid = "mock_blob_pid"

    def setup_mocks(
        self,
        mock_workspace_api,
        mock_blob,
        mock_blob_system_api,
        user,
        owner=None,
    ) -> None:
        """setup_mocks"""
        mock_workspace = MagicMock()

        mock_workspace_api.get_all_workspaces_with_read_access_by_user.return_value = (
            [mock_workspace] if user == owner else []
        )

        mock_blob_object = MagicMock()
        mock_blob_object.user_id = owner.id if owner else user.id
        mock_blob_object.workspace = mock_workspace

        mock_blob.get_by_id.return_value = mock_blob_object

        mock_blob_system_api.set_pid_for_blob.return_value = self.mock_blob_pid

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    def test_superuser_can_access(
        self,
        mock_workspace_api,
        mock_blob,
        mock_blob_system_api,
    ):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)

        self.setup_mocks(
            mock_workspace_api, mock_blob, mock_blob_system_api, user
        )
        self.assertEqual(
            blob_api.set_pid_for_blob("mock_blob_id", "mock_blob_pid", user),
            self.mock_blob_pid,
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    def test_registered_user_not_owner_cannot_access(
        self,
        mock_workspace_api,
        mock_blob,
        mock_blob_system_api,
    ):
        """test_registered_user_not_owner_cannot_access"""
        user = create_mock_user("1")
        owner = create_mock_user("2")

        self.setup_mocks(
            mock_workspace_api, mock_blob, mock_blob_system_api, user, owner
        )

        with self.assertRaises(AccessControlError):
            blob_api.set_pid_for_blob("mock_blob_id", "mock_blob_pid", user)

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    def test_registered_user_and_owner_can_access(
        self,
        mock_workspace_api,
        mock_blob,
        mock_blob_system_api,
    ):
        """test_registered_user_and_owner_can_access"""
        user = create_mock_user("1")

        self.setup_mocks(
            mock_workspace_api, mock_blob, mock_blob_system_api, user
        )
        self.assertEqual(
            blob_api.set_pid_for_blob("mock_blob_id", "mock_blob_pid", user),
            self.mock_blob_pid,
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "Blob")
    @patch.object(main_acl, "workspace_api")
    def test_anonymous_user_cannot_access(
        self,
        mock_workspace_api,
        mock_blob,
        mock_blob_system_api,
    ):
        """test_anonymous_user_without_perm_cannot_access"""
        user = create_mock_user("1", is_anonymous=True)

        self.setup_mocks(
            mock_workspace_api, mock_blob, mock_blob_system_api, user
        )

        with self.assertRaises(AccessControlError):
            blob_api.set_pid_for_blob("mock_blob_id", "mock_blob_pid", user)
