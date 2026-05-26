"""Unit tests for core_linked_records_app.components.pid_path.api"""

from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.components.pid_path import (
    api as pid_path_api,
)
from core_linked_records_app.components.pid_path.models import PidPath
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import (
    api as template_api,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests import mocks
from core_linked_records_app import settings


class TestGetByTemplateId(TestCase):
    """Test Get By Template Id"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1")
        self.mock_template = mocks.MockDocument()
        self.mock_template.user = self.mock_user.id
        self.kwargs = {
            "template": self.mock_template,
            "user": self.mock_user,
        }

    @patch.object(PidPath, "get_by_template")
    def test_get_by_template_failure_raises_api_error(
        self, mock_get_by_template
    ):
        """test_get_by_template_failure_raises_api_error"""

        mock_get_by_template.side_effect = Exception(
            "mock_get_by_template_exception"
        )

        with self.assertRaises(ApiError):
            pid_path_api.get_by_template(**self.kwargs)

    @patch.object(PidPath, "__init__")
    @patch.object(PidPath, "get_by_template")
    def test_pid_path_init_failure_raises_api_error(
        self, mock_get_by_template, mock_pid_path
    ):
        """test_pid_path_init_failure_raises_api_error"""

        mock_get_by_template.return_value = None
        mock_pid_path.side_effect = Exception("mock_pid_path_exception")

        with self.assertRaises(ApiError):
            pid_path_api.get_by_template(**self.kwargs)

    @patch("core_linked_records_app.components.pid_path.api.PidPath")
    def test_returns_new_pid_path_if_not_exists(
        self,
        mock_pid_path_class,  # noqa, pylint: disable=unused-argument
    ):
        """test_returns_new_pid_path_if_not_exists"""
        mock_qs = Mock()
        mock_qs.exists.return_value = False

        mock_pid_path_class.get_by_template.return_value = mock_qs

        pid_path_api.get_by_template(**self.kwargs)

        mock_pid_path_class.assert_called_once_with(
            template=self.mock_template, path=settings.PID_PATH
        )

    @patch.object(template_api, "get_by_id")
    @patch.object(PidPath, "get_by_template")
    def test_returns_pid_path_if_exists(
        self,
        mock_get_by_template,
        mock_get_by_id,
    ):
        """test_returns_pid_path_if_exists"""
        mock_template = mocks.MockTemplate()
        mock_template.pk = 123
        mock_qs = Mock()
        mock_qs.exists.return_value = True
        mock_get_by_template.return_value = mock_qs
        mock_get_by_id.return_value = mock_template

        self.assertEqual(pid_path_api.get_by_template(**self.kwargs), mock_qs)


class TestGetAll(TestCase):
    """Test Get All"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()
        self.mock_request.user = create_mock_user("1")

    @patch.object(template_api, "get_all")
    def test_template_api_get_all_failure_raises_api_error(self, mock_get_all):
        """test_template_api_get_all_failure_raises_api_error"""

        mock_get_all.side_effect = Exception("mock_get_all_exception")

        with self.assertRaises(ApiError):
            pid_path_api.get_all(self.mock_request)

    @patch.object(PidPath, "get_all_by_template_list")
    @patch.object(template_api, "get_all")
    def test_get_all_by_template_list_failure_raises_api_error(
        self, mock_get_all, mock_get_all_by_template_list
    ):
        """test_get_all_by_template_list_failure_raises_api_error"""

        mock_get_all.return_value = []
        mock_get_all_by_template_list.side_effect = Exception(
            "mock_get_all_exception"
        )

        with self.assertRaises(ApiError):
            pid_path_api.get_all(self.mock_request)

    @patch.object(PidPath, "get_all_by_template_list")
    @patch.object(template_api, "get_all")
    def test_returns_get_all_by_template_list_output(
        self, mock_get_all, mock_get_all_by_template_list
    ):
        """test_returns_get_all_by_template_list_output"""

        expected_result = "mock_get_all_by_template_list"
        mock_get_all.return_value = []
        mock_get_all_by_template_list.return_value = expected_result

        self.assertEqual(
            pid_path_api.get_all(self.mock_request), expected_result
        )
