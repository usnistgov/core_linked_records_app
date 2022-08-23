""" Permission tests for core_linked_records_app.rest.pid.views
"""
from unittest import TestCase
from unittest.mock import patch

from rest_framework import status
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_explore_common_app.components.query import api as query_api
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.data import api as data_api
from core_linked_records_app.rest.pid import views as pid_views
from tests import mocks


class TestRetrieveDataPidGet(TestCase):
    """Test Retrieve Data Pid Get"""

    @patch.object(data_api, "get_pid_for_data")
    def test_anonymous_returns_200(self, mock_get_pid_for_data):
        """test_anonymous_returns_200"""

        mock_get_pid_for_data.return_value = "mock_pid"

        response = RequestMock.do_request_get(
            pid_views.RetrieveDataPIDView.as_view(),
            None,
            data={"data_id": "mock_data_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_pid_for_data")
    def test_authenticated_returns_200(self, mock_get_pid_for_data):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        mock_get_pid_for_data.return_value = "mock_pid"

        response = RequestMock.do_request_get(
            pid_views.RetrieveDataPIDView.as_view(),
            mock_user,
            data={"data_id": "mock_data_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_pid_for_data")
    def test_staff_returns_200(self, mock_get_pid_for_data):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_get_pid_for_data.return_value = "mock_pid"

        response = RequestMock.do_request_get(
            pid_views.RetrieveDataPIDView.as_view(),
            mock_user,
            data={"data_id": "mock_data_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRetrieveBlobPidGet(TestCase):
    """Test Retrieve Blob Pid Get"""

    @patch.object(blob_api, "get_pid_for_blob")
    def test_anonymous_returns_200(self, mock_get_pid_for_blob):
        """test_anonymous_returns_"""

        mock_get_pid_for_blob.return_value = mocks.MockLocalId()

        response = RequestMock.do_request_get(
            pid_views.RetrieveBlobPIDView.as_view(),
            None,
            data={"blob_id": "mock_blob_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_api, "get_pid_for_blob")
    def test_authenticated_returns_200(self, mock_get_pid_for_blob):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        mock_get_pid_for_blob.return_value = mocks.MockLocalId()

        response = RequestMock.do_request_get(
            pid_views.RetrieveBlobPIDView.as_view(),
            mock_user,
            data={"blob_id": "mock_blob_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_api, "get_pid_for_blob")
    def test_staff_returns_200(self, mock_get_pid_for_blob):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_get_pid_for_blob.return_value = mocks.MockLocalId()

        response = RequestMock.do_request_get(
            pid_views.RetrieveBlobPIDView.as_view(),
            mock_user,
            data={"blob_id": "mock_blob_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRetrieveListPidPost(TestCase):
    """Test Retrieve List Pid Post"""

    def setUp(self) -> None:
        self.mock_data_source = dict(
            query_options=dict(),
            order_by_field="",
            authentication=dict(
                auth_type="oauth2", params={"access_token": "mock_access_token"}
            ),
            capabilities={"url_pid": True},
        )

    def send_post_request(self, mock_query_get_by_id, mock_send_get_request, user):
        """send_post_request"""

        mock_query_get_by_id.return_value = mocks.MockQuery(
            data_sources=[self.mock_data_source]
        )
        mock_send_get_request.return_value = mocks.MockResponse(json_data=[None])

        return RequestMock.do_request_post(
            pid_views.RetrieveListPIDView.as_view(),
            user,
            data={"query_id": "mock_query_id", "data_source_index": "0"},
            content_type=None,
        )

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_anonymous_returns_200(self, mock_query_get_by_id, mock_send_get_request):
        """test_anonymous_returns_200"""

        response = self.send_post_request(
            mock_query_get_by_id, mock_send_get_request, None
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_authenticated_returns_200(
        self, mock_query_get_by_id, mock_send_get_request
    ):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        response = self.send_post_request(
            mock_query_get_by_id, mock_send_get_request, mock_user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_staff_returns_200(self, mock_query_get_by_id, mock_send_get_request):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        response = self.send_post_request(
            mock_query_get_by_id, mock_send_get_request, mock_user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
