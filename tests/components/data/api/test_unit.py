""" Unit tests for core_linked_records_app.components.data.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from django.http import HttpRequest

from core_main_app.commons import exceptions
from core_main_app.components.data import api as main_data_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_linked_records_app.components.data import api as pid_data_api
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from tests import mocks


class TestGetDataByPid(TestCase):
    """Test Get Data By Pid"""

    def setUp(self) -> None:
        mock_pid = "mock_pid"
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"pid": mock_pid, "request": mock_request}

    @patch.object(main_data_api, "execute_query")
    def test_execute_query_failure_raises_api_error(self, mock_execute_query):
        """test_execute_query_failure_raises_api_error"""

        mock_execute_query.side_effect = Exception("mock_execute_query_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_no_result_raise_does_not_exist_error(self, mock_execute_query):
        """test_no_result_raise_does_not_exist_error"""

        mock_execute_query.return_value = []

        with self.assertRaises(exceptions.DoesNotExist):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_several_results_raise_api_error(self, mock_execute_query):
        """test_several_results_raise_api_error"""

        mock_execute_query.return_value = ["item_a", "item_b"]

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_single_result_is_returned(self, mock_execute_query):
        """test_single_result_is_returned"""

        expected_result = "single_item"
        mock_execute_query.return_value = [expected_result]

        result = pid_data_api.get_data_by_pid(**self.mock_kwargs)
        self.assertEquals(result, expected_result)


class TestGetPidsForDataList(TestCase):
    """Test Get Pids For Data List"""

    def setUp(self) -> None:
        mock_data_id_list = ["mock_id_a", "mock_id_b"]
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"data_id_list": mock_data_id_list, "request": mock_request}

    @patch.object(pid_data_api, "get_pid_for_data")
    def test_get_pid_for_data_failure_raises_api_error(self, mock_get_pid_for_data):
        """test_get_pid_for_data_failure_raises_api_error"""

        mock_get_pid_for_data.side_effect = Exception("mock_get_by_id_list_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pids_for_data_list(**self.mock_kwargs)

    @patch.object(pid_data_api, "get_pid_for_data")
    def test_get_pid_for_data_returns_list(self, mock_get_pid_for_data):
        """test_get_pid_for_data_returns_list"""

        mock_get_pid_for_data.side_effect = lambda data_id, req: f"{data_id}_pid"

        self.assertListEqual(
            pid_data_api.get_pids_for_data_list(**self.mock_kwargs),
            [f"{data_id}_pid" for data_id in self.mock_kwargs["data_id_list"]],
        )


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
    def test_get_by_id_failure_raises_api_error(self, mock_get_by_id):
        """test_get_by_id_failure_raises_api_error"""

        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_get_by_template_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template
    ):
        """test_get_by_template_failure_raises_api_error"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.side_effect = Exception("mock_get_by_template_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_is_key_list_in_dictionary_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template, mock_is_dot_notation_in_dictionary
    ):
        """test_is_key_list_in_dictionary_failure_raises_api_error"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_is_dot_notation_in_dictionary_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_is_dot_notation_in_dictionary_failure_raises_api_error(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_is_dot_notation_in_dictionary_failure_raises_api_error"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_is_dot_notation_in_dictionary_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_pid_xpath_not_in_document_returns_none(
        self, mock_get_by_id, mock_get_by_template, mock_is_dot_notation_in_dictionary
    ):
        """test_pid_xpath_not_in_document_returns_none"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_is_dot_notation_in_dictionary.return_value = False

        self.assertIsNone(pid_data_api.get_pid_for_data(**self.mock_kwargs))

    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_get_value_from_dot_notation_failure_raises_api_error(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
    ):
        """test_get_value_from_dot_notation_failure_raises_api_error"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_get_value_from_dot_notation.return_value = True
        mock_is_dot_notation_in_dictionary.side_effect = Exception(
            "mock_get_dict_value_from_key_list_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_invalid_pid_raises_api_error(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
        mock_is_valid_pid_value,
    ):
        """test_invalid_pid_raises_api_error"""

        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_is_dot_notation_in_dictionary.return_value = True
        mock_get_value_from_dot_notation.return_value = "mock_pid"
        mock_is_valid_pid_value.return_value = False

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "is_valid_pid_value")
    @patch.object(pid_data_api, "is_dot_notation_in_dictionary")
    @patch.object(pid_data_api, "get_value_from_dot_notation")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(main_data_api, "get_by_id")
    def test_returns_get_value_from_dot_notation_output(
        self,
        mock_get_by_id,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_dot_notation_in_dictionary,
        mock_is_valid_pid_value,
    ):
        """test_returns_get_value_from_dot_notation_output"""

        expected_result = "mock_pid"
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_is_dot_notation_in_dictionary.return_value = True
        mock_get_value_from_dot_notation.return_value = expected_result
        mock_is_valid_pid_value.return_value = True

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertEquals(result, expected_result)
