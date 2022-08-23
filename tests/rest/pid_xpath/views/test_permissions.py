""" Permission tests for core_linked_records_app.rest.pid_xpath.views
"""
from unittest import TestCase
from unittest.mock import patch

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_linked_records_app.rest.pid_xpath import views as pid_xpath_views


class TestPidXpathListViewGet(TestCase):
    """Test Pid Xpath List View Get"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_200(self):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_returns_200(self):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathListViewPost(TestCase):
    """Test Pid Xpath List View Post"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_post(
            pid_xpath_views.PidXpathListView.as_view(),
            None,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(ListCreateAPIView, "post")
    def test_authenticated_returns_201(self, mock_view_post):
        """test_authenticated_returns_201"""

        mock_user = create_mock_user("1")

        mock_view_post.return_value = Response(status=status.HTTP_201_CREATED)
        response = RequestMock.do_request_post(
            pid_xpath_views.PidXpathListView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(ListCreateAPIView, "post")
    def test_staff_returns_201(self, mock_view_post):
        """test_staff_returns_201"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_view_post.return_value = Response(status=status.HTTP_201_CREATED)
        response = RequestMock.do_request_post(
            pid_xpath_views.PidXpathListView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPidXpathDetailViewGet(TestCase):
    """Test Pid Xpath Detail View Get"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), None, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "get")
    def test_authenticated_returns_200(self, mock_view_get):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        mock_view_get.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), mock_user, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(RetrieveUpdateDestroyAPIView, "get")
    def test_staff_returns_200(self, mock_view_get):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_view_get.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), mock_user, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathDetailViewPatch(TestCase):
    """Test Pid Xpath Detail View Patch"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_patch(
            pid_xpath_views.PidXpathDetailView.as_view(),
            None,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "patch")
    def test_authenticated_returns_200(self, mock_view_patch):
        """test_authenticated_returns_200"""

        mock_user = create_mock_user("1")

        mock_view_patch.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_patch(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(RetrieveUpdateDestroyAPIView, "patch")
    def test_staff_returns_200(self, mock_view_patch):
        """test_staff_returns_200"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_view_patch.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_patch(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathDetailViewDelete(TestCase):
    """Test Pid Xpath Detail View Delete"""

    def test_anonymous_returns_403(self):
        """test_anonymous_returns_403"""

        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "delete")
    def test_authenticated_returns_204(self, mock_view_delete):
        """test_authenticated_returns_204"""

        mock_user = create_mock_user("1")

        mock_view_delete.return_value = Response(status=status.HTTP_204_NO_CONTENT)
        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(RetrieveUpdateDestroyAPIView, "delete")
    def test_staff_returns_204(self, mock_view_delete):
        """test_staff_returns_204"""

        mock_user = create_mock_user("1", is_staff=True)

        mock_view_delete.return_value = Response(status=status.HTTP_204_NO_CONTENT)
        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
