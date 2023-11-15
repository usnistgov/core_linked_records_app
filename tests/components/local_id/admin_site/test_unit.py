""" Unit tests for PidPath admin site
"""
from unittest import TestCase
from unittest.mock import Mock

from core_linked_records_app.components.local_id.admin_site import (
    CustomLocalIdAdmin,
)


class TestCustomLocalIdAdminHasAddPermission(TestCase):
    """Test has_add_permission in CustomLocalIdAdmin view"""

    def test_cannot_add_item(self):
        """test_cannot_add_item"""
        custom_local_id_model_admin = CustomLocalIdAdmin(Mock(), Mock())
        self.assertFalse(
            custom_local_id_model_admin.has_add_permission(None, None)
        )


class TestCustomLocalIdAdminHasChangePermission(TestCase):
    """Test has_change_permission in CustomLocalIdAdmin view"""

    def test_cannot_edit_item(self):
        """test_cannot_edit_item"""
        custom_local_id_model_admin = CustomLocalIdAdmin(Mock(), Mock())
        self.assertFalse(
            custom_local_id_model_admin.has_change_permission(None, None)
        )
