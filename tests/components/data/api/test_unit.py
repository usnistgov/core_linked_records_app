"""Unit tests for core_linked_records_app.components.data.api"""

from unittest import TestCase
from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_main_app.components.data import api as main_data_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from django.http import HttpRequest

from core_linked_records_app.components.data import (
    access_control as pid_data_acl,
)
from core_linked_records_app.components.data import api as pid_data_api
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.utils.exceptions import MultiplePidError
from tests import mocks


class TestGetDataByPid(TestCase):
    """Test Get Data By Pid"""

    def setUp(self) -> None:
        mock_pid = "mock_pid"
        self.mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.mock_user

        self.mock_kwargs = {"pid": mock_pid, "request": mock_request}

    @patch.object(pid_path_api, "get_all")
    def test_pid_path_get_all_failure_raises_api_error(self, mock_get_all):
        """test_pid_path_get_all_failure_raises_api_error"""

        mock_get_all.side_effect = Exception("mock_get_all_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_execute_query_failure_raises_api_error(
        self, mock_get_all, mock_execute_json_query
    ):
        """test_execute_query_failure_raises_api_error"""

        mock_get_all.return_value = []
        mock_execute_json_query.side_effect = Exception(
            "mock_execute_json_query_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_no_result_raise_does_not_exist_error(
        self, mock_get_all, mock_execute_json_query
    ):
        """test_no_result_raise_does_not_exist_error"""

        mock_get_all.return_value = []
        mock_execute_json_query.return_value = []

        with self.assertRaises(exceptions.DoesNotExist):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_several_results_raise_api_error(
        self, mock_get_all, mock_execute_json_query
    ):
        """test_several_results_raise_api_error"""

        mock_get_all.return_value = []
        mock_execute_json_query.return_value = ["item_a", "item_b"]

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_single_result_is_returned(
        self, mock_get_all, mock_execute_json_query
    ):
        """test_single_result_is_returned"""

        mock_get_all.return_value = []
        expected_result = mocks.MockData()
        expected_result.user_id = self.mock_user.id
        mock_execute_json_query.return_value = [expected_result]

        result = pid_data_api.get_data_by_pid(**self.mock_kwargs)
        self.assertEqual(result, expected_result)


class TestGetPidForData(TestCase):
    """Test Get Pid For Data"""

    def setUp(self) -> None:
        mock_data_id = mocks.MockData().pk
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"data_id": mock_data_id, "request": mock_request}

        self.mock_global_data = mocks.MockData()

    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_get_by_id_failure_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
    ):
        """test_get_by_id_failure_raises_api_error"""

        mock_check_can_read_document.return_value = True
        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_get_by_template_failure_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
    ):
        """test_get_by_template_failure_raises_api_error"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.side_effect = Exception(
            "mock_get_by_template_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_is_key_list_in_dictionary_failure_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_is_key_list_in_dictionary_failure_raises_api_error"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_is_dot_notation_in_dictionary_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_is_dot_notation_in_dictionary_failure_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_is_dot_notation_in_dictionary_failure_raises_api_error"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_is_dot_notation_in_dictionary_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_pid_path_not_in_document_returns_none(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_pid_path_not_in_document_returns_none"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_is_dot_notation_in_dictionary.return_value = False

        self.assertIsNone(pid_data_api.get_pid_for_data(**self.mock_kwargs))

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_get_value_from_dot_notation_failure_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_get_value_from_dot_notation_failure_raises_api_error"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_get_value_from_dot_notation.return_value = True
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_get_dict_value_from_key_list_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_invalid_pid_raises_api_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
        mock_is_valid_pid_value,
    ):
        """test_invalid_pid_raises_api_error"""

        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_is_dot_notation_in_dictionary.return_value = True
        mock_get_value_from_dot_notation.return_value = "mock_pid"
        mock_is_valid_pid_value.return_value = False

        self.assertIsNone(pid_data_api.get_pid_for_data(**self.mock_kwargs))

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_returns_get_value_from_dot_notation_output(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
        mock_is_valid_pid_value,
    ):
        """test_returns_get_value_from_dot_notation_output"""

        mock_check_can_read_document.return_value = True
        expected_result = "mock_pid"
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = [mocks.MockPidPath()]
        mock_is_dot_notation_in_dictionary.return_value = True
        mock_get_value_from_dot_notation.return_value = expected_result
        mock_is_valid_pid_value.return_value = True

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertEqual(result, expected_result)


class TestGetPidForDataMultiPath(TestCase):
    """Test Get Pid For Data with multiple paths"""

    def setUp(self) -> None:
        mock_data_id = mocks.MockData().pk
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"data_id": mock_data_id, "request": mock_request}
        self.mock_global_data = mocks.MockData()

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_single_valid_pid_in_first_path_returns_pid(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
        mock_get_value_from_dot_notation,
        mock_is_valid_pid_value,
    ):
        """Test single valid PID in first path is returned"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data

        # Mock multiple PidPath objects
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_1.path = "path1"
        mock_pid_path_2 = mocks.MockPidPath()
        mock_pid_path_2.path = "path2"
        mock_get_by_template.return_value = [mock_pid_path_1, mock_pid_path_2]

        # First path has PID, second doesn't
        mock_is_dot_notation_in_dictionary.side_effect = [True, False]
        mock_get_value_from_dot_notation.return_value = "valid_pid"
        mock_is_valid_pid_value.return_value = True

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertEqual(result, "valid_pid")

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_valid_pid_in_second_path_returns_pid(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
        mock_get_value_from_dot_notation,
        mock_is_valid_pid_value,
    ):
        """Test valid PID in second path is returned"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data

        # Mock multiple PidPath objects
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_1.path = "path1"
        mock_pid_path_2 = mocks.MockPidPath()
        mock_pid_path_2.path = "path2"
        mock_get_by_template.return_value = [mock_pid_path_1, mock_pid_path_2]

        # First path doesn't have PID, second does
        mock_is_dot_notation_in_dictionary.side_effect = [False, True]
        mock_get_value_from_dot_notation.return_value = "valid_pid_path2"
        mock_is_valid_pid_value.return_value = True

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertEqual(result, "valid_pid_path2")

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_multiple_valid_pids_raises_error(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
        mock_get_value_from_dot_notation,
        mock_is_valid_pid_value,
    ):
        """Test error when multiple valid PIDs exist across paths"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data

        # Mock multiple PidPath objects
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_1.path = "path1"
        mock_pid_path_2 = mocks.MockPidPath()
        mock_pid_path_2.path = "path2"
        mock_get_by_template.return_value = [mock_pid_path_1, mock_pid_path_2]

        # Both paths have PIDs
        mock_is_dot_notation_in_dictionary.side_effect = [True, True]
        mock_get_value_from_dot_notation.side_effect = ["pid1", "pid2"]
        mock_is_valid_pid_value.return_value = True

        with self.assertRaises(MultiplePidError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_path_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    @patch.object(pid_data_acl, "Data")
    @patch.object(pid_data_acl, "check_can_read_document")
    def test_no_pid_in_any_path_returns_none(
        self,
        mock_check_can_read_document,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
        mock_get_value_from_dot_notation,
        mock_is_valid_pid_value,
    ):
        """Test returns None when no PID exists in any path"""
        mock_check_can_read_document.return_value = True
        mock_get_by_id.return_value = self.mock_global_data

        # Mock multiple PidPath objects
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_1.path = "path1"
        mock_pid_path_2 = mocks.MockPidPath()
        mock_pid_path_2.path = "path2"
        mock_get_by_template.return_value = [mock_pid_path_1, mock_pid_path_2]

        # Neither path has PID
        mock_is_dot_notation_in_dictionary.side_effect = [False, False]

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertIsNone(result)


class TestGetDataByPidMultiPath(TestCase):
    """Test Get Data By Pid with multiple paths"""

    def setUp(self) -> None:
        mock_pid = "mock_pid"
        self.mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = self.mock_user
        self.mock_request = mock_request
        self.mock_kwargs = {"pid": mock_pid, "request": mock_request}

    @patch.object(main_data_api, "execute_json_query")
    @patch.object(pid_path_api, "get_all")
    def test_search_matches_multiple_paths(
        self, mock_get_all, mock_execute_json_query
    ):
        """Test PID search uses $or condition across multiple paths"""
        # Mock multiple paths
        mock_pid_path_1 = mocks.MockPidPath()
        mock_pid_path_1.path = "path1"
        mock_pid_path_2 = mocks.MockPidPath()
        mock_pid_path_2.path = "path2"
        mock_get_all.return_value = [mock_pid_path_1, mock_pid_path_2]

        expected_result = mocks.MockData()
        expected_result.user_id = self.mock_user.id
        mock_execute_json_query.return_value = [expected_result]

        result = pid_data_api.get_data_by_pid(**self.mock_kwargs)

        # Verify query was called with $or condition
        mock_execute_json_query.assert_called_once()
        call_args = mock_execute_json_query.call_args
        query = call_args[0][0]

        # Check $or condition exists
        self.assertIn("$or", query)
        self.assertEqual(result, expected_result)
