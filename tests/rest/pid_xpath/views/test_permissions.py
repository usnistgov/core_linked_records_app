""" Permission tests for core_linked_records_app.rest.pid_xpath.views
"""
from unittest import TestCase

from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from unittest.mock import patch

from core_linked_records_app.rest.pid_xpath import views as pid_xpath_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestPidXpathListViewGet(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_200(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_returns_200(self):
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathListView.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathListViewPost(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_post(
            pid_xpath_views.PidXpathListView.as_view(),
            None,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(ListCreateAPIView, "post")
    def test_authenticated_returns_201(self, mock_view_post):
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
        mock_user = create_mock_user("1", is_staff=True)

        mock_view_post.return_value = Response(status=status.HTTP_201_CREATED)
        response = RequestMock.do_request_post(
            pid_xpath_views.PidXpathListView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPidXpathDetailViewGet(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), None, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "get")
    def test_authenticated_returns_200(self, mock_view_get):
        mock_user = create_mock_user("1")

        mock_view_get.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), mock_user, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(RetrieveUpdateDestroyAPIView, "get")
    def test_staff_returns_200(self, mock_view_get):
        mock_user = create_mock_user("1", is_staff=True)

        mock_view_get.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_get(
            pid_xpath_views.PidXpathDetailView.as_view(), mock_user, param={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathDetailViewPatch(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_patch(
            pid_xpath_views.PidXpathDetailView.as_view(),
            None,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "patch")
    def test_authenticated_returns_200(self, mock_view_patch):
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
        mock_user = create_mock_user("1", is_staff=True)

        mock_view_patch.return_value = Response(status=status.HTTP_200_OK)
        response = RequestMock.do_request_patch(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
            data={"xpath": "mock.xpath", "template": "mock_template_id"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPidXpathDetailViewDelete(TestCase):
    def test_anonymous_returns_403(self):
        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RetrieveUpdateDestroyAPIView, "delete")
    def test_authenticated_returns_204(self, mock_view_delete):
        mock_user = create_mock_user("1")

        mock_view_delete.return_value = Response(status=status.HTTP_204_NO_CONTENT)
        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(RetrieveUpdateDestroyAPIView, "delete")
    def test_staff_returns_204(self, mock_view_delete):
        mock_user = create_mock_user("1", is_staff=True)

        mock_view_delete.return_value = Response(status=status.HTTP_204_NO_CONTENT)
        response = RequestMock.do_request_delete(
            pid_xpath_views.PidXpathDetailView.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
