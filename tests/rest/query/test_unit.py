""" Unit test for REST query views
"""
from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app.rest.query import views as query_views
from tests import mocks


class TestRetrieveQueryPidListViewPost(TestCase):
    """Unit tests for post function of RetrieveQueryPidListView class"""

    def setUp(self) -> None:
        """setUp"""
        self.test_view = query_views.RetrieveQueryPidListView()
        self.mock_request = mocks.MockRequest()

    @patch.object(query_views, "execute_local_pid_query")
    def test_execute_local_pid_query_error_returns_500(
        self, mock_execute_local_pid_query
    ):
        """test_execute_local_pid_query_error_returns_500"""
        mock_execute_local_pid_query.side_effect = Exception(
            "mock_execute_local_pid_query_exception"
        )

        response = self.test_view.post(self.mock_request)
        self.assertEqual(response.status_code, 500)

    @patch.object(query_views, "execute_local_pid_query")
    def test_success_returns_200(self, mock_execute_local_pid_query):
        """test_success_returns_200"""
        mock_execute_local_pid_query.return_value = [
            "mock_data_pid" for _ in range(5)
        ]

        response = self.test_view.post(self.mock_request)
        self.assertEqual(response.status_code, 200)

    @patch.object(query_views, "execute_local_pid_query")
    def test_success_returns_execute_local_pid_query(
        self, mock_execute_local_pid_query
    ):
        """test_success_returns_execute_local_pid_query"""
        expected_result = ["mock_data_pid" for _ in range(5)]
        mock_execute_local_pid_query.return_value = expected_result

        response = self.test_view.post(self.mock_request)
        self.assertEqual(response.data, expected_result)
