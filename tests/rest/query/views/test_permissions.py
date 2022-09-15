""" Permission tests for core_linked_records_app.rest.query.views
"""
from unittest import TestCase
from unittest.mock import patch

from rest_framework import status
from rest_framework.response import Response

from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_linked_records_app.rest.query import views as query_views


class TestExecuteLocalPIDQueryViewGet(TestCase):
    """Test Execute Local PID Query View Get"""

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_200(self, mock_execute_query):
        """test_anonymous_returns_200"""

        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_get(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_200(self, mock_execute_query):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_get(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_200(self, mock_execute_query):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_get(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestExecuteLocalPIDQueryViewPost(TestCase):
    """Test Execute Local PID Query View Post"""

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_200(self, mock_execute_query):
        """test_anonymous_returns_200"""

        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_post(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_200(self, mock_execute_query):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_post(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_200(self, mock_execute_query):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        response = RequestMock.do_request_post(
            query_views.ExecuteLocalPIDQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# FIXME cannot import oai_pmh_harvester in INSTALLED_APPS
# class TestExecuteOaiPmhPIDQueryViewGet(TestCase):
#     """ Test Execute Oai Pmh PID Query View Get """
#
#     def test_anonymous_returns_200(self):
#         pass
#
#     @patch.object(ExecuteQueryView, "execute_query")
#     def test_authenticated_returns_200(self, mock_execute_query):
#         mock_user = create_mock_user("1")
#         mock_execute_query.return_value = Response(status=status.HTTP_200_OK)
#
#         response = RequestMock.do_request_get(
#             query_views.ExecuteOaiPmhPIDQueryView.as_view(),
#             mock_user,
#             data={"query": "{}"},
#         )
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_staff_returns_200(self):
#         pass
#
#
# class TestExecuteOaiPmhPIDQueryViewPost(TestCase):
#     """ Test Execute Oai Pmh PID Query View Post """
#     def test_anonymous_returns_200(self):
#         pass
#
#     @patch.object(ExecuteQueryView, "execute_query")
#     def test_authenticated_returns_200(self, mock_execute_query):
#         mock_user = create_mock_user("1")
#         mock_execute_query.return_value = Response(status=status.HTTP_200_OK)
#
#         response = RequestMock.do_request_post(
#             query_views.ExecuteOaiPmhPIDQueryView.as_view(),
#             mock_user,
#             data={"query": "{}"},
#         )
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_staff_returns_200(self):
#         pass
