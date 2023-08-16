""" Unit tests for core_linked_records_app.system.pid_xpath.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.system.pid_xpath import (
    api as pid_xpath_system_api,
)


class TestGetPidXpathByTemplate(TestCase):
    """Test get_pid_xpath_by_template method"""

    @patch(
        "core_linked_records_app.system.pid_xpath.api.PidXpath.get_by_template"
    )
    def test_get_by_template_is_called(self, mock_get_by_template):
        """Test get_by_template is called"""
        mock_template = "mock_template"

        pid_xpath_system_api.get_pid_xpath_by_template(mock_template)
        mock_get_by_template.assert_called_with(mock_template)

    @patch("core_linked_records_app.system.pid_xpath.api.PidXpath.__new__")
    @patch(
        "core_linked_records_app.system.pid_xpath.api.PidXpath.get_by_template"
    )
    def test_get_by_template_none_returns_pid_xpath(
        self, mock_get_by_template, mock_pid_xpath
    ):
        """If get_by_template returns None, the PidXpath returned is the default one."""
        expected_result = Mock(spec=PidXpath)
        mock_get_by_template.return_value = None
        mock_pid_xpath.return_value = expected_result

        result = pid_xpath_system_api.get_pid_xpath_by_template(
            "mock_template"
        )
        self.assertEqual(result, expected_result)

    @patch(
        "core_linked_records_app.system.pid_xpath.api.PidXpath.get_by_template"
    )
    def test_returns_get_by_template_if_not_none(self, mock_get_by_template):
        """If get_by_template is not None, the PidXpath returned is get_by_template."""
        expected_result = "mock_result"
        mock_get_by_template.return_value = expected_result

        result = pid_xpath_system_api.get_pid_xpath_by_template(
            "mock_template"
        )
        self.assertEqual(result, expected_result)
