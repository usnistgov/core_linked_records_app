""" Unit tests for core_linked_records_app.rest.query.views
"""
from unittest import TestCase
from unittest.mock import patch

from core_explore_oaipmh_app.rest.query.views import ExecuteQueryView
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.rest.query import views as query_views
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import (
    AbstractExecuteLocalQueryView,
)
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_api,
)
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
        expected_result = [
            {"pid": mock_data_pid} for _ in range(5) if _ % 2 == 0
        ]

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


class TestExecuteOaiPmhPIDQueryViewBuildQuery(TestCase):
    """Test Execute Local PID Query View Build Query"""

    @patch.object(ExecuteQueryView, "build_query")
    @patch.object(pid_xpath_api, "get_all")
    def test_add_pid_query_if_init_query_has_and(
        self, mock_pid_xpath_get_all, mock_build_query
    ):
        """test_add_pid_query_if_init_query_has_and"""

        mock_pid_xpath_get_all.return_value = []
        mock_build_query.return_value = {}

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.build_query(
            "mock_query", ["mock_template"], ["mock_registry"]
        )

        self.assertEqual(len(result["$and"]), 2)

    @patch.object(ExecuteQueryView, "build_query")
    @patch.object(pid_xpath_api, "get_all")
    def test_append_pid_query_if_init_query_has_no_and(
        self, mock_pid_xpath_get_all, mock_build_query
    ):
        """test_append_pid_query_if_init_query_has_no_and"""

        mock_pid_xpath_get_all.return_value = []
        mock_build_query.return_value = {"$and": ["query1", "query2"]}

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        test_view.request = mocks.MockRequest()
        result = test_view.build_query(
            "mock_query", ["mock_template"], ["mock_registry"]
        )

        self.assertEqual(len(result["$and"]), 3)


class TestExecuteOaiPmhPIDQueryViewExecuteJsonQuery(TestCase):
    """Test Execute Local PID Query View Execute Raw Query"""

    @patch.object(oai_record_api, "execute_json_query")
    def test_undefined_pid_xpath_list_raises_error(self, mock_execute_query):
        """test_no_data_returns_empty_list"""

        mock_execute_query.return_value = []

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        test_view.request = mocks.MockRequest()
        test_view.pid_xpath_list = None

        with self.assertRaises(Exception):
            test_view.execute_json_query("mock_query", "order_by_field")

    @patch.object(oai_record_api, "execute_json_query")
    def test_no_data_returns_empty_list(self, mock_execute_query):
        """test_no_data_returns_empty_list"""

        mock_execute_query.return_value = []

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        test_view.request = mocks.MockRequest()
        test_view.pid_xpath_list = []

        result = test_view.execute_json_query("mock_query", "order_by_field")

        self.assertEqual(result, [])

    @patch.object(query_views, "get_value_from_dot_notation")
    @patch.object(pid_xpath_api, "get_by_template")
    @patch.object(oai_record_api, "execute_json_query")
    def test_returns_data_with_valid_pid(
        self,
        mock_execute_query,
        mock_get_by_template,
        mock_get_value_from_dot_notation,
    ):
        """test_returns_data_with_valid_pid"""

        mock_data_pid = "mock_data_pid"
        mock_execute_query.return_value = [mocks.MockData() for _ in range(5)]
        mock_get_by_template.return_value = mocks.MockPidXpath()
        # Return `mock_data_pid` every time the call count is odd (3 times for a list
        # of 5 elements, at index 0, 2 and 4), otherwise returns None.
        mock_get_value_from_dot_notation.side_effect = (
            lambda d, p: mock_data_pid
            if mock_get_value_from_dot_notation.call_count % 2
            else None
        )
        expected_result = [{"pid": mock_data_pid} for _ in range(3)]

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        test_view.request = mocks.MockRequest()
        test_view.pid_xpath_list = []
        result = test_view.execute_json_query("mock_query", "order_by_field")

        self.assertEqual(result, expected_result)


class TestExecuteOaiPmhPIDQueryViewBuildResponse(TestCase):
    """Test Execute Local PID Query View Build Response"""

    def test_returns_list_of_data_pid(self):
        """test_returns_list_of_data_pid"""

        mock_data_pid = "mock_data_pid"
        mock_data_list = [{"pid": mock_data_pid} for _ in range(5)]
        expected_result = [mock_data_pid for _ in range(5)]

        test_view = query_views.ExecuteOaiPmhPIDQueryView()
        response = test_view.build_response(mock_data_list)

        self.assertEqual(response.data, expected_result)
