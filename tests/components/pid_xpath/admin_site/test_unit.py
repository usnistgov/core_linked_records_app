""" Unit tests for PidXPath admin site
"""
from unittest import TestCase
from unittest.mock import Mock

from core_linked_records_app.components.pid_xpath.admin_site import (
    CustomPidXpathAdmin,
)


class TestCustomPidXpathAdminHasAddPermission(TestCase):
    """Test has_add_permission in CustomPidXpathAdmin view"""

    def test_can_add_item(self):
        """test_can_add_item"""
        custom_pid_xpath_model_admin = Mock(spec=CustomPidXpathAdmin)
        self.assertTrue(
            custom_pid_xpath_model_admin.has_add_permission(None, None)
        )
