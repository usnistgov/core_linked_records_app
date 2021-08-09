""" Permission tests for core_linked_records_app.rest.providers.views
"""
from unittest import TestCase

import json
from rest_framework import status
from unittest.mock import patch

from core_linked_records_app import settings
from core_linked_records_app.rest.providers import views as providers_views
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.rest.data.serializers import DataSerializer
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests import mocks


class TestProviderRecordViewPost(TestCase):
    @staticmethod
    def _send_request(mock_provider_manager_get, mock_user):
        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            create_result=mocks.MockResponse(status_code=status.HTTP_201_CREATED)
        )
        return RequestMock.do_request_post(
            providers_views.ProviderRecordView.as_view(),
            mock_user,
            param={
                "provider": "local",
                "record": f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
            },
        )

    @patch.object(ProviderManager, "get")
    def test_anonymous_returns_201(self, mock_provider_manager_get):

        response = self._send_request(mock_provider_manager_get, None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(ProviderManager, "get")
    def test_authenticated_returns_201(self, mock_provider_manager_get):
        mock_user = create_mock_user("1")

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(ProviderManager, "get")
    def test_staff_returns_201(self, mock_provider_manager_get):
        mock_user = create_mock_user("1", is_staff=True)

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestProviderRecordViewPut(TestCase):
    @staticmethod
    def _send_request(mock_provider_manager_get, mock_user):

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            update_result=mocks.MockResponse()
        )
        return RequestMock.do_request_put(
            providers_views.ProviderRecordView.as_view(),
            mock_user,
            param={
                "provider": "local",
                "record": f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
            },
        )

    @patch.object(ProviderManager, "get")
    def test_anonymous_returns_200(self, mock_provider_manager_get):
        response = self._send_request(mock_provider_manager_get, None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(ProviderManager, "get")
    def test_authenticated_returns_200(self, mock_provider_manager_get):
        mock_user = create_mock_user("1")

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(ProviderManager, "get")
    def test_staff_returns_200(self, mock_provider_manager_get):
        mock_user = create_mock_user("1", is_staff=True)

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProviderRecordViewGet(TestCase):
    @staticmethod
    def _send_request(
        mock_provider_manager_get, mock_get_data_by_pid, mock_data_serializer, mock_user
    ):
        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(content=json.dumps({"url": "mock_url"}))
        )
        mock_get_data_by_pid.return_value = None
        mock_data_serializer.return_value = mocks.MockSerializer()
        return RequestMock.do_request_get(
            providers_views.ProviderRecordView.as_view(),
            mock_user,
            param={
                "provider": "local",
                "record": f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
            },
        )

    @patch.object(DataSerializer, "__new__")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_anonymous_returns_200(
        self, mock_provider_manager_get, mock_get_data_by_pid, mock_data_serializer
    ):
        response = self._send_request(
            mock_provider_manager_get,
            mock_get_data_by_pid,
            mock_data_serializer,
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "__new__")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_authenticated_returns_200(
        self, mock_provider_manager_get, mock_get_data_by_pid, mock_data_serializer
    ):
        mock_user = create_mock_user("1")

        response = self._send_request(
            mock_provider_manager_get,
            mock_get_data_by_pid,
            mock_data_serializer,
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "__new__")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_staff_returns_200(
        self, mock_provider_manager_get, mock_get_data_by_pid, mock_data_serializer
    ):
        mock_user = create_mock_user("1", is_staff=True)

        response = self._send_request(
            mock_provider_manager_get,
            mock_get_data_by_pid,
            mock_data_serializer,
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProviderRecordViewDelete(TestCase):
    @staticmethod
    def _send_request(mock_provider_manager_get, mock_user):
        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            delete_result=mocks.MockResponse(status_code=status.HTTP_204_NO_CONTENT)
        )
        return RequestMock.do_request_delete(
            providers_views.ProviderRecordView.as_view(),
            mock_user,
            param={
                "provider": "local",
                "record": f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
            },
        )

    @patch.object(ProviderManager, "get")
    def test_anonymous_returns_204(self, mock_provider_manager_get):
        response = self._send_request(mock_provider_manager_get, None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(ProviderManager, "get")
    def test_authenticated_returns_204(self, mock_provider_manager_get):
        mock_user = create_mock_user("1")

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(ProviderManager, "get")
    def test_staff_returns_204(self, mock_provider_manager_get):
        mock_user = create_mock_user("1", is_staff=True)

        response = self._send_request(mock_provider_manager_get, mock_user)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
