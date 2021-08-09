""" Unit tests for core_linked_records_app.components.data.api
"""
from unittest import TestCase

from django.http import HttpRequest
from unittest.mock import patch, Mock

from core_linked_records_app.components.data import api as pid_data_api
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_main_app.commons import exceptions
from core_main_app.components.data import api as main_data_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests import mocks


class TestGetDataByPid(TestCase):
    def setUp(self) -> None:
        mock_pid = "mock_pid"
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"pid": mock_pid, "request": mock_request}

    @patch.object(main_data_api, "execute_query")
    def test_execute_query_failure_raises_api_error(self, mock_execute_query):
        mock_execute_query.side_effect = Exception("mock_execute_query_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_no_result_raise_does_not_exist_error(self, mock_execute_query):
        mock_execute_query.return_value = []

        with self.assertRaises(exceptions.DoesNotExist):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_several_results_raise_api_error(self, mock_execute_query):
        mock_execute_query.return_value = ["item_a", "item_b"]

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_data_by_pid(**self.mock_kwargs)

    @patch.object(main_data_api, "execute_query")
    def test_single_result_is_returned(self, mock_execute_query):
        expected_result = "single_item"
        mock_execute_query.return_value = [expected_result]

        result = pid_data_api.get_data_by_pid(**self.mock_kwargs)
        self.assertEquals(result, expected_result)


class TestGetPidsForDataList(TestCase):
    def setUp(self) -> None:
        mock_data_id_list = ["mock_id_a", "mock_id_b"]
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"data_id_list": mock_data_id_list, "request": mock_request}

    @patch.object(main_data_api, "get_by_id_list")
    def test_get_by_id_list_failure_raises_api_error(self, mock_get_by_id_list):
        mock_get_by_id_list.side_effect = Exception("mock_get_by_id_list_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pids_for_data_list(**self.mock_kwargs)

    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id_list")
    def test_get_by_template_id_failure_raises_api_error(
        self,
        mock_get_by_id_list,
        mock_get_by_template_id,
    ):
        mock_get_by_id_list.return_value = [mocks.MockData()]
        mock_get_by_template_id.side_effect = Exception(
            "mock_get_by_template_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pids_for_data_list(**self.mock_kwargs)

    @patch.object(pid_data_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id_list")
    def test_get_dict_value_from_key_list_failure_raises_api_error(
        self,
        mock_get_by_id_list,
        mock_get_by_template_id,
        mock_get_dict_value_from_key_list,
    ):
        mock_get_by_id_list.return_value = [mocks.MockData()]
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.side_effect = Exception(
            "mock_get_dict_value_from_key_list_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pids_for_data_list(**self.mock_kwargs)

    @patch.object(pid_data_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id_list")
    def test_list_of_pid_does_not_contain_none_values(
        self,
        mock_get_by_id_list,
        mock_get_by_template_id,
        mock_get_dict_value_from_key_list,
    ):
        mock_get_by_id_list.return_value = [mocks.MockData()]
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.return_value = None

        result = pid_data_api.get_pids_for_data_list(**self.mock_kwargs)
        self.assertEquals(result, [])

    @patch.object(pid_data_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id_list")
    def test_returns_list_of_pid(
        self,
        mock_get_by_id_list,
        mock_get_by_template_id,
        mock_get_dict_value_from_key_list,
    ):
        mock_pid = "mock_pid"
        expected_result = [mock_pid for _ in range(5)]
        mock_get_by_id_list.return_value = [mocks.MockData() for _ in range(5)]
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.return_value = mock_pid

        result = pid_data_api.get_pids_for_data_list(**self.mock_kwargs)
        self.assertEquals(result, expected_result)


class TestGetPidForData(TestCase):
    def setUp(self) -> None:
        mock_data_id = mocks.MockData().pk
        mock_user = create_mock_user("1")
        mock_request = Mock(spec=HttpRequest)
        mock_request.user = mock_user

        self.mock_kwargs = {"data_id": mock_data_id, "request": mock_request}

        self.mock_global_data = mocks.MockData()

    @patch.object(main_data_api, "get_by_id")
    def test_get_by_id_failure_raises_api_error(self, mock_get_by_id):
        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id")
    def test_get_by_template_id_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template_id
    ):
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template_id.side_effect = Exception(
            "mock_get_by_template_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id")
    def test_get_dict_value_from_key_list_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template_id, mock_get_dict_value_from_key_list
    ):
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.side_effect = Exception(
            "mock_get_dict_value_from_key_list_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            pid_data_api.get_pid_for_data(**self.mock_kwargs)

    @patch.object(pid_data_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(main_data_api, "get_by_id")
    def test_returns_get_dict_value_from_key_list_output(
        self, mock_get_by_id, mock_get_by_template_id, mock_get_dict_value_from_key_list
    ):
        expected_result = "mock_pid"
        mock_get_by_id.return_value = self.mock_global_data
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.return_value = expected_result

        result = pid_data_api.get_pid_for_data(**self.mock_kwargs)
        self.assertEquals(result, expected_result)
