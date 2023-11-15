""" Unit tests for core_linked_records_app.rest.query.views
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.utils import query as query_utils
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError, CoreError
from core_main_app.components.data import api as data_api
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_api,
)
from tests import mocks


class TestBuildPidQuery(TestCase):
    """Test Execute Local PID Query View Build Query"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(pid_path_api, "get_all")
    def test_add_pid_query_if_init_query_has_and(self, mock_pid_path_get_all):
        """test_add_pid_query_if_init_query_has_and"""

        mock_pid_path_get_all.return_value = []
        mock_function = Mock()
        mock_function.return_value = {"mock_key": "mock_value"}

        result = query_utils.build_pid_query(
            "mock_query", mock_function, self.mock_request
        )

        self.assertEqual(len(result["$and"]), 2)

    @patch.object(pid_path_api, "get_all")
    def test_append_pid_query_if_init_query_has_no_and(
        self, mock_pid_path_get_all
    ):
        """test_append_pid_query_if_init_query_has_no_and"""

        mock_pid_path_get_all.return_value = []
        mock_function = Mock()
        mock_function.return_value = {"$and": ["query1", "query2"]}

        result = query_utils.build_pid_query(
            "mock_query", mock_function, self.mock_request
        )

        self.assertEqual(len(result["$and"]), 3)


class TestExecutePidQuery(TestCase):
    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(query_utils, "build_pid_query")
    def test_build_pid_query_unauthorized_raises_acl_error(
        self, mock_build_pid_query
    ):
        mock_build_pid_query.side_effect = AccessControlError(
            "mock_build_pid_query_exception"
        )

        with self.assertRaises(AccessControlError):
            query_utils.execute_pid_query(
                "mock_query", Mock(), Mock(), self.mock_request
            )

    @patch.object(query_utils, "build_pid_query")
    def test_execute_fn_unauthorized_raises_acl_error(
        self, mock_build_pid_query
    ):
        mock_build_pid_query.return_value = "mock_pid_query"
        mock_execute_fn = Mock()
        mock_execute_fn.side_effect = AccessControlError(
            "mock_execute_fn_exception"
        )

        with self.assertRaises(AccessControlError):
            query_utils.execute_pid_query(
                "mock_query", Mock(), mock_execute_fn, self.mock_request
            )

    @patch.object(query_utils, "build_pid_query")
    def test_build_pid_query_fail_raises_api_error(self, mock_build_pid_query):
        mock_build_pid_query.side_effect = Exception(
            "mock_build_pid_query_exception"
        )

        with self.assertRaises(ApiError):
            query_utils.execute_pid_query(
                "mock_query", Mock(), Mock(), self.mock_request
            )

    @patch.object(query_utils, "build_pid_query")
    def test_execute_fn_fail_raises_api_error(self, mock_build_pid_query):
        mock_build_pid_query.return_value = "mock_pid_query"
        mock_execute_fn = Mock()
        mock_execute_fn.side_effect = Exception("mock_execute_fn_exception")

        with self.assertRaises(ApiError):
            query_utils.execute_pid_query(
                "mock_query", Mock(), mock_execute_fn, self.mock_request
            )

    @patch.object(query_utils, "build_pid_query")
    def test_success_returns_execute_fn(self, mock_build_pid_query):
        mock_build_pid_query.return_value = "mock_pid_query"
        expected_results = "mock_results"
        mock_execute_fn = Mock()
        mock_execute_fn.return_value = expected_results

        results = query_utils.execute_pid_query(
            "mock_query", Mock(), mock_execute_fn, self.mock_request
        )
        self.assertEqual(results, expected_results)


class TestExecuteLocalQuery(TestCase):
    """Test Execute Local PID Query View Execute Raw Query"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(data_api, "execute_json_query")
    def test_no_data_returns_empty_list(self, mock_execute_query):
        """test_no_data_returns_empty_list"""

        mock_execute_query.return_value = []

        result = query_utils.execute_local_query(
            "mock_query", self.mock_request
        )

        self.assertEqual(result, [])

    @patch.object(query_utils, "is_valid_pid_value")
    @patch.object(query_utils, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
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
        mock_get_by_template.return_value = mocks.MockPidPath()
        mock_get_value_from_dot_notation.return_value = mock_data_pid
        # Return True every time the call count is odd (3 times for a list of 5
        # elements, at index 0, 2 and 4).
        mock_is_valid_pid_value.side_effect = (
            lambda p, n, f: mock_is_valid_pid_value.call_count % 2
        )
        expected_result = [mock_data_pid for _ in range(5) if _ % 2 == 0]

        result = query_utils.execute_local_query(
            "mock_query", self.mock_request
        )

        self.assertEqual(result, expected_result)


class TestExecuteLocalPidQuery(TestCase):
    @patch.object(query_utils, "execute_pid_query")
    def test_returns_execute_pid_query_result(self, mock_execute_pid_query):
        expected_result = "mock_result"
        mock_execute_pid_query.return_value = expected_result

        result = query_utils.execute_local_pid_query(
            "mock_query", mocks.MockRequest()
        )
        self.assertEqual(result, expected_result)


class TestExecuteOaiPmhQuery(TestCase):
    """Test Execute Local PID Query View Execute Raw Query"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(query_utils, "settings")
    def test_no_oaipmh_harvester_raises_core_error(self, mock_settings):
        mock_settings.INSTALLED_APPS = ["core_explore_oaipmh_app"]

        with self.assertRaises(CoreError):
            query_utils.execute_oaipmh_query("mock_query", self.mock_request)

    @patch.object(oai_record_api, "execute_json_query")
    def test_no_data_returns_empty_list(self, mock_execute_query):
        """test_no_data_returns_empty_list"""

        mock_execute_query.return_value = []

        result = query_utils.execute_oaipmh_query(
            "mock_query", self.mock_request
        )

        self.assertEqual(result, [])

    @patch.object(query_utils, "get_value_from_dot_notation")
    @patch.object(pid_path_api, "get_by_template")
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
        mock_get_by_template.return_value = mocks.MockPidPath()
        # Return `mock_data_pid` every time the call count is odd (3 times for a list
        # of 5 elements, at index 0, 2 and 4), otherwise returns None.
        mock_get_value_from_dot_notation.side_effect = (
            lambda d, p: mock_data_pid
            if mock_get_value_from_dot_notation.call_count % 2
            else None
        )
        expected_result = [mock_data_pid for _ in range(3)]

        result = query_utils.execute_oaipmh_query(
            "mock_query", self.mock_request
        )

        self.assertEqual(result, expected_result)


class TestExecuteOaiPmhPidQuery(TestCase):
    @patch.object(query_utils, "execute_pid_query")
    @patch.object(query_utils, "settings")
    def test_no_explore_oaipmh_raises_core_error(
        self, mock_settings, mock_execute_pid_query
    ):
        expected_result = "mock_result"
        mock_execute_pid_query.return_value = expected_result
        mock_settings.INSTALLED_APPS = []

        with self.assertRaises(CoreError):
            query_utils.execute_oaipmh_pid_query(
                "mock_query", mocks.MockRequest()
            )

    @patch.object(query_utils, "execute_pid_query")
    def test_returns_execute_pid_query_result(self, mock_execute_pid_query):
        expected_result = "mock_result"
        mock_execute_pid_query.return_value = expected_result

        result = query_utils.execute_oaipmh_pid_query(
            "mock_query", mocks.MockRequest()
        )
        self.assertEqual(result, expected_result)
