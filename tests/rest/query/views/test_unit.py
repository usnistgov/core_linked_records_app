""" Unit tests for core_linked_records_app.rest.query.views
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.rest.query import views as query_views
from tests import mocks


class TestExecuteLocalPIDQueryViewBuildQuery(TestCase):
    """Test Execute Local PID Query View Build Query"""

    @patch.object(AbstractExecuteLocalQueryView, "build_query")
    @patch.object(pid_xpath_api, "get_all")
    def test_add_pid_query_if_init_query_has_and(
        self, mock_pid_xpath_get_all, mock_build_query
    ):
        """test_add_pid_query_if_init_query_has_and"""

        mock_pid_xpath_get_all.return_value = []
        mock_build_query.return_value = {}

        test_view = query_views.ExecuteLocalPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.build_query("mock_query")

        self.assertEqual(len(result["$and"]), 2)

    @patch.object(AbstractExecuteLocalQueryView, "build_query")
    @patch.object(pid_xpath_api, "get_all")
    def test_append_pid_query_if_init_query_has_no_and(
        self, mock_pid_xpath_get_all, mock_build_query
    ):
        """test_append_pid_query_if_init_query_has_no_and"""

        mock_pid_xpath_get_all.return_value = []
        mock_build_query.return_value = {"$and": ["query1", "query2"]}

        test_view = query_views.ExecuteLocalPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.build_query("mock_query")

        self.assertEqual(len(result["$and"]), 3)


class TestExecuteLocalPIDQueryViewExecuteRawQuery(TestCase):
    """Test Execute Local PID Query View Execute Raw Query"""

    @patch.object(data_api, "execute_json_query")
    def test_no_data_returns_empty_list(self, mock_execute_query):
        """test_no_data_returns_empty_list"""

        mock_execute_query.return_value = []

        test_view = query_views.ExecuteLocalPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.execute_raw_query("mock_query", "order_by_field")

        self.assertEqual(result, [])

    @patch.object(query_views, "is_valid_pid_value")
    @patch.object(query_views, "get_value_from_dot_notation")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(data_api, "execute_json_query")
    def test_returns_data_with_valid_pid(
        self,
        mock_execute_query,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
        mock_is_valid_pid_value,
    ):
        """test_returns_data_with_valid_pid"""

        mock_data_pid = "mock_data_pid"
        mock_execute_query.return_value = [mocks.MockData() for _ in range(5)]
        mock_get_by_template.return_value = mocks.MockPidXpath()
        mock_get_value_from_dot_notation.return_value = mock_data_pid
        # Return True every time the call count is odd (3 times for a list of 5
        # elements, at index 0, 2 and 4).
        mock_is_valid_pid_value.side_effect = (
            lambda p, n, f: mock_is_valid_pid_value.call_count % 2
        )
        expected_result = [{"pid": mock_data_pid} for _ in range(5) if _ % 2 == 0]

        test_view = query_views.ExecuteLocalPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.execute_raw_query("mock_query", "order_by_field")

        self.assertEqual(result, expected_result)


class TestExecuteLocalPIDQueryViewBuildResponse(TestCase):
    """Test Execute Local PID Query View Build Response"""

    def test_returns_list_of_data_pid(self):
        """test_returns_list_of_data_pid"""

        mock_data_pid = "mock_data_pid"
        mock_data_list = [{"pid": mock_data_pid} for _ in range(5)]
        expected_result = [mock_data_pid for _ in range(5)]

        test_view = query_views.ExecuteLocalPIDQueryView()
        response = test_view.build_response(mock_data_list)

        self.assertEqual(response.data, expected_result)
