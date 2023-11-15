""" Unit tests for PidPath admin site
"""
from unittest import TestCase
from unittest.mock import Mock

from core_linked_records_app.components.pid_path.admin_site import (
    CustomPidPathAdmin,
)


class TestCustomPidPathAdminHasAddPermission(TestCase):
    """Test has_add_permission in CustomPidPathAdmin view."""

    def test_can_add_item(self):
        """test_can_add_item"""
        custom_pid_path_model_admin = Mock(spec=CustomPidPathAdmin)
        self.assertTrue(
            custom_pid_path_model_admin.has_add_permission(None, None)
        )
