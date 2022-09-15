""" Unit tests for core_linked_records_app.rest.blob.views
"""
from unittest import TestCase
from unittest.mock import patch

from rest_framework import status

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.blob.views import BlobList
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.rest.blob import views as blob_views
from tests import mocks


class TestBlobUploadWithPIDViewPost(TestCase):
    """Test Blob Upload With PID View Post"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()
        self.mock_request.user = create_mock_user("1", is_superuser=True)
        self.mock_request.POST = dict()

    def test_pid_none_returns_500(self):
        """test_pid_none_returns_500"""

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(local_id_api, "get_by_name")
    def test_local_pid_get_by_name_fails_returns_500(self, mock_get_by_name):
        """test_local_pid_get_by_name_fails_returns_500"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(local_id_api, "get_by_name")
    def test_local_pid_get_by_name_succeeds_returns_500(self, mock_get_by_name):
        """test_local_pid_get_by_name_succeeds_returns_500"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.return_value = None

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(BlobList, "post")
    @patch.object(local_id_api, "get_by_name")
    def test_super_post_fails_returns_500(self, mock_get_by_name, mock_blob_list_post):
        """test_super_post_fails_returns_500"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.side_effect = DoesNotExist("mock_get_by_name_does_not_exist")
        mock_blob_list_post.side_effect = Exception("mock_blob_list_post_exception")

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(BlobList, "post")
    @patch.object(local_id_api, "get_by_name")
    def test_super_post_returns_400_returns_400(
        self, mock_get_by_name, mock_blob_list_post
    ):
        """test_super_post_returns_400_returns_400"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.side_effect = DoesNotExist("mock_get_by_name_does_not_exist")
        mock_blob_list_post.return_value = mocks.MockResponse(
            status_code=status.HTTP_400_BAD_REQUEST
        )

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 400)

    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(BlobList, "post")
    @patch.object(local_id_api, "get_by_name")
    def test_set_pid_for_blob_fails_returns_500(
        self, mock_get_by_name, mock_blob_list_post, mock_set_pid_for_blob
    ):
        """test_set_pid_for_blob_fails_returns_500"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.side_effect = DoesNotExist("mock_get_by_name_does_not_exist")
        mock_blob_list_post.return_value = mocks.MockResponse(
            status_code=status.HTTP_201_CREATED, data={"id": "mock_blob_id"}
        )
        mock_set_pid_for_blob.side_effect = Exception("mock_set_pid_for_blob_exception")

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(BlobList, "post")
    @patch.object(local_id_api, "get_by_name")
    def test_success_returns_201(
        self, mock_get_by_name, mock_blob_list_post, mock_set_pid_for_blob
    ):
        """test_success_returns_201"""

        self.mock_request.POST["pid"] = "mock_pid"
        mock_get_by_name.side_effect = DoesNotExist("mock_get_by_name_does_not_exist")
        mock_blob_list_post.return_value = mocks.MockResponse(
            status_code=status.HTTP_201_CREATED, data={"id": "mock_blob_id"}
        )
        mock_set_pid_for_blob.return_value = None

        test_view = blob_views.BlobUploadWithPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 201)
