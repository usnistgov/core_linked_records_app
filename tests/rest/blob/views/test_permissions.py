""" Permission tests for core_linked_records_app.rest.blob.views
"""
from unittest import TestCase

from rest_framework import status
from unittest.mock import patch

from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.rest.blob import views as blob_views
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.blob.views import BlobList
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests import mocks


class TestBlobUploadWithPIDViewPost(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_post(
            blob_views.BlobUploadWithPIDView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            blob_views.BlobUploadWithPIDView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_403(self):
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            blob_views.BlobUploadWithPIDView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(BlobList, "post")
    @patch.object(local_id_api, "get_by_name")
    def test_superuser_returns_201(
        self, mock_get_by_name, mock_blob_list_post, mock_set_pid_for_blob
    ):
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        mock_get_by_name.side_effect = DoesNotExist("mock_get_by_name_exception")
        mock_blob_list_post.return_value = mocks.MockResponse(
            data={"id": "mock_id"}, status_code=status.HTTP_201_CREATED
        )
        mock_set_pid_for_blob.return_value = None

        response = RequestMock.do_request_post(
            blob_views.BlobUploadWithPIDView.as_view(),
            mock_user,
            data={"pid": "mock_pid"},
            content_type=None,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
