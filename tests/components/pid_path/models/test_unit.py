""" Unit tests for core_linked_records_app.components.pid_path.models
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.core.exceptions import ObjectDoesNotExist

from core_linked_records_app.components.pid_path.models import PidPath
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template.models import Template


class TestPidPathGetAll(TestCase):
    """Unit tests for `PidPath.get_all` method."""

    @patch.object(PidPath, "objects")
    def test_pid_path_all_failure_raises_model_error(self, mock_pid_path):
        """test_pid_path_all_failure_raises_model_error"""

        mock_pid_path.all.side_effect = Exception(
            "mock_pid_path_all_exception"
        )

        with self.assertRaises(ModelError):
            PidPath.get_all()

    @patch.object(PidPath, "objects")
    def test_returns_pid_path_all_output(self, mock_pid_path):
        """test_returns_pid_path_all_output"""

        expected_result = "mock_pid_path_all"
        mock_pid_path.all.return_value = expected_result

        self.assertEqual(PidPath.get_all(), expected_result)


class TestPidPathGetByTemplateList(TestCase):
    """Unit tests for `PidPath.get_all_by_template_list` method."""

    @patch.object(PidPath, "objects")
    def test_pid_path_filter_failure_raises_model_error(self, mock_pid_path):
        """test_pid_path_filter_failure_raises_model_error"""

        mock_pid_path.filter.side_effect = Exception(
            "mock_pid_path_filter_exception"
        )

        with self.assertRaises(ModelError):
            PidPath.get_all_by_template_list("mock_template_list")

    @patch.object(PidPath, "objects")
    def test_returns_pid_path_filter_output(self, mock_pid_path):
        """test_returns_pid_path_filter_output"""

        expected_result = "mock_pid_path_filter"
        mock_pid_path.filter.return_value = expected_result

        self.assertEqual(
            PidPath.get_all_by_template_list("mock_template_list"),
            expected_result,
        )


class TestPidPathGetByTemplate(TestCase):
    """Unit tests for `PidPath.get_by_template` method."""

    @patch.object(PidPath, "objects")
    def test_pid_path_get_does_not_exists_returns_none(self, mock_pid_path):
        """test_pid_path_get_does_not_exists_returns_none"""

        mock_pid_path.get.side_effect = ObjectDoesNotExist()

        self.assertIsNone(PidPath.get_by_template("mock_template"))

    @patch.object(PidPath, "objects")
    def test_pid_path_get_raises_model_error(self, mock_pid_path):
        """test_pid_path_get_raises_model_error"""

        mock_pid_path.get.side_effect = Exception(
            "mock_pid_path_get_exception"
        )

        with self.assertRaises(ModelError):
            PidPath.get_by_template("mock_template")

    @patch.object(PidPath, "objects")
    def test_returns_pid_path_get_output(self, mock_pid_path):
        """test_returns_pid_path_get_output"""

        expected_result = "mock_pid_path_get"
        mock_pid_path.get.return_value = expected_result

        self.assertEqual(
            PidPath.get_by_template("mock_template"), expected_result
        )


class TestPidPathStr(TestCase):
    """Unit tests for `PidPath.__str__` method."""

    def test_str_is_correct(self):
        mock_path = MagicMock()
        mock_template = Template()
        pid_path_object = PidPath()
        pid_path_object.path = mock_path
        pid_path_object.template = mock_template

        self.assertEqual(
            pid_path_object.__str__(),
            f"PID path '{mock_path}' for template '{mock_template}'",
        )
