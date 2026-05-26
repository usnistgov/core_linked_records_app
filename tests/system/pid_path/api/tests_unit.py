"""Unit tests for core_linked_records_app.system.pid_path.api"""

from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app import settings
from core_linked_records_app.system.pid_path import api as pid_path_system_api
from core_linked_records_app.components.pid_path.models import PidPath
from tests import mocks


class TestGetPidPathByTemplate(TestCase):
    """Test get_pid_path_by_template method"""

    @patch(
        "core_linked_records_app.system.pid_path.api.PidPath.get_by_template"
    )
    def test_get_by_template_is_called(self, mock_get_by_template):
        """Test get_by_template is called"""
        mock_template = "mock_template"

        pid_path_system_api.get_pid_path_by_template(mock_template)
        mock_get_by_template.assert_called_with(mock_template)

    @patch("core_linked_records_app.system.pid_path.api.PidPath")
    def test_get_by_template_none_returns_pid_path(self, mock_pid_path):
        """If get_by_template returns None, the PidPath returned is the default one."""
        expected_result = Mock(spec=PidPath)
        mock_pid_path.return_value = expected_result

        mock_qs = Mock()
        mock_qs.exists.return_value = False
        mock_pid_path.get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_pid_path_by_template("mock_template")
        self.assertEqual(result, expected_result)

    @patch(
        "core_linked_records_app.system.pid_path.api.PidPath.get_by_template"
    )
    def test_returns_get_by_template_if_not_none(self, mock_get_by_template):
        """If get_by_template is not None, the PidPath returned is get_by_template."""
        expected_result = "mock_result"
        mock_template = mocks.MockTemplate()
        mock_template.pk = 123
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        mock_qs.first.return_value = expected_result
        mock_get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_pid_path_by_template("mock_template")
        self.assertEqual(result, expected_result)

    @patch.object(PidPath, "get_by_template")
    def test_single_path_returns_path_object(self, mock_get_by_template):
        mock_template = mocks.MockTemplate()
        mock_pid_path = mocks.MockPidPath()
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        mock_qs.first.return_value = mock_pid_path
        mock_get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_pid_path_by_template(mock_template)

        self.assertEqual(result, mock_pid_path)

    @patch.object(PidPath, "get_by_template")
    def test_multiple_paths_returns_first(self, mock_get_by_template):
        mock_template = mocks.MockTemplate()
        mock_first = mocks.MockPidPath()
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        mock_qs.first.return_value = mock_first
        mock_get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_pid_path_by_template(mock_template)

        self.assertEqual(result, mock_first)

    @patch("core_linked_records_app.system.pid_path.api.PidPath")
    def test_no_paths_returns_default(self, mock_pid_path_class):
        mock_template = mocks.MockTemplate()
        mock_template.pk = 123
        mock_qs = Mock()
        mock_qs.exists.return_value = False
        mock_pid_path_class.get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_pid_path_by_template(mock_template)

        mock_pid_path_class.assert_called_once_with(
            template=mock_template, path=settings.PID_PATH
        )
        self.assertEqual(result, mock_pid_path_class.return_value)


class TestGetAllPidPathsByTemplate(TestCase):
    """Test get_all_pid_paths_by_template always returns a plain list"""

    @patch.object(PidPath, "get_by_template")
    def test_paths_exist_returns_list(self, mock_get_by_template):
        mock_template = mocks.MockTemplate()
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_2 = mocks.MockPidPath()
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        # list() is called on the queryset — make it iterable
        mock_qs.__iter__ = Mock(
            return_value=iter([mock_pid_path_1, mock_pid_path_2])
        )
        mock_get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_all_pid_paths_by_template(
            mock_template
        )

        self.assertIsInstance(result, list)
        self.assertEqual(result, [mock_pid_path_1, mock_pid_path_2])

    @patch("core_linked_records_app.system.pid_path.api.PidPath")
    def test_no_paths_returns_list_with_default(self, mock_pid_path_class):
        mock_template = mocks.MockTemplate()
        mock_template.pk = 123
        mock_qs = Mock()
        mock_qs.exists.return_value = False
        mock_pid_path_class.get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_all_pid_paths_by_template(
            mock_template
        )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        mock_pid_path_class.assert_called_once_with(
            template=mock_template, path=settings.PID_PATH
        )

    @patch.object(PidPath, "get_by_template")
    def test_return_is_always_list_not_queryset(self, mock_get_by_template):
        """Caller code must be able to use len() and indexing unconditionally."""
        mock_template = mocks.MockTemplate()
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        mock_qs.__iter__ = Mock(return_value=iter([mocks.MockPidPath()]))
        mock_get_by_template.return_value = mock_qs

        result = pid_path_system_api.get_all_pid_paths_by_template(
            mock_template
        )

        # Must be a plain list — not a Mock, not a QuerySet
        self.assertIsInstance(result, list)
        self.assertIsNotNone(result[0])
        self.assertGreater(len(result), 0)
