""" Unit tests for core_linked_records_app.rest.providers.views
"""
import json
from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app import settings
from core_linked_records_app.rest.providers import views as providers_views
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.data.serializers import DataSerializer
from tests import mocks


class TestProviderRecordViewPost(TestCase):
    """Test Provider Record View Post"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    def test_invalid_prefix_returns_500(self):
        """test_invalid_prefix_returns_500"""

        test_view = providers_views.ProviderRecordView()
        response = test_view.post(
            self.mock_request, "mock_provider", "mock_prefix/mock_record"
        )

        self.assertEqual(response.status_code, 500)

    def test_invalid_record_returns_500(self):
        """test_invalid_record_returns_500"""

        test_view = providers_views.ProviderRecordView()
        response = test_view.post(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/@@@@@",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_provider_manager_get_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_get_fails_returns_500"""

        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.post(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_provider_manager_create_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_create_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            create_exc=Exception("mock_provider_manager_create_exception")
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.post(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_success_returns_200(self, mock_provider_manager_get):
        """test_success_returns_200"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            create_result=mocks.MockResponse()
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.post(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 200)


class TestProviderRecordViewPut(TestCase):
    """Test Provider Record View Put"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(ProviderManager, "get")
    def test_provider_manager_get_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_get_fails_returns_500"""

        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.put(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_provider_manager_update_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_update_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            update_exc=Exception("mock_provider_manager_update_exception")
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.put(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_success_returns_200(self, mock_provider_manager_get):
        """test_success_returns_200"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            update_result=mocks.MockResponse()
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.put(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 200)


class TestProviderRecordViewGet(TestCase):
    """Test Provider Record View Get"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(ProviderManager, "get")
    def test_provider_manager_get_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_get_fails_returns_500"""

        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_provider_manager_get_record_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_get_record_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_exc=Exception("mock_provider_manager_get_exception")
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_data_by_pid_fails_returns_500(
        self, mock_provider_manager_get, mock_get_data_by_pid
    ):
        """test_get_data_by_pid_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = Exception(
            "mock_get_data_by_pid_exception"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(DataSerializer, "__new__")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_data_serializer_fails_returns_500(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_data_serializer,
    ):
        """test_data_serializer_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.return_value = mocks.MockData()
        mock_data_serializer.side_effect = Exception(
            "mock_data_serializer_exception"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(DataSerializer, "__new__")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_data_success_returns_200(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_data_serializer,
    ):
        """test_get_data_success_returns_200"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = mocks.MockData()
        mock_data_serializer.return_value = mocks.MockSerializer()

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 200)

    @patch.object(providers_views, "get_blob_by_pid")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_blob_by_pid_fails_returns_500(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_get_blob_by_pid,
    ):
        """test_get_blob_by_pid_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = DoesNotExist(
            "mock_get_data_by_pid_does_not_exist"
        )
        mock_get_blob_by_pid.side_effect = Exception(
            "mock_get_blob_by_pid_exception"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(providers_views, "get_blob_by_pid")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_blob_by_pid_access_control_error_returns_403(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_get_blob_by_pid,
    ):
        """test_get_blob_by_pid_access_control_error_returns_403"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = DoesNotExist(
            "mock_get_data_by_pid_does_not_exist"
        )
        mock_get_blob_by_pid.side_effect = AccessControlError(
            "mock_get_blob_by_pid_access_control_error"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 403)

    @patch.object(providers_views, "get_blob_by_pid")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_blob_by_pid_deos_not_exist_returns_404(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_get_blob_by_pid,
    ):
        """test_get_blob_by_pid_deos_not_exist_returns_404"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = DoesNotExist(
            "mock_get_data_by_pid_does_not_exist"
        )
        mock_get_blob_by_pid.side_effect = DoesNotExist(
            "mock_get_blob_by_pid_does_not_exist"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 404)

    @patch.object(providers_views, "get_file_http_response")
    @patch.object(providers_views, "get_blob_by_pid")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_file_http_response_fails_returns_500(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_get_blob_by_pid,
        mock_get_file_http_response,
    ):
        """test_get_file_http_response_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = DoesNotExist(
            "mock_get_data_by_pid_does_not_exist"
        )
        mock_get_blob_by_pid.return_value = mocks.MockBlob()
        mock_get_file_http_response.side_effect = Exception(
            "mock_get_file_http_response"
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(providers_views, "get_file_http_response")
    @patch.object(providers_views, "get_blob_by_pid")
    @patch.object(providers_views, "get_data_by_pid")
    @patch.object(ProviderManager, "get")
    def test_get_file_http_response_success_returns_200(
        self,
        mock_provider_manager_get,
        mock_get_data_by_pid,
        mock_get_blob_by_pid,
        mock_get_file_http_response,
    ):
        """test_get_file_http_response_success_returns_200"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            get_result=mocks.MockResponse(
                content=json.dumps({"url": "mock_url"})
            )
        )
        mock_get_data_by_pid.side_effect = DoesNotExist(
            "mock_get_data_by_pid_does_not_exist"
        )
        mock_get_blob_by_pid.return_value = mocks.MockBlob()
        mock_get_file_http_response.return_value = mocks.MockResponse()

        test_view = providers_views.ProviderRecordView()
        response = test_view.get(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 200)


class TestProviderRecordViewDelete(TestCase):
    """Test Provider Record View Delete"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()

    @patch.object(ProviderManager, "get")
    def test_provider_manager_get_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_get_fails_returns_500"""

        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )
        test_view = providers_views.ProviderRecordView()
        response = test_view.delete(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_provider_manager_update_fails_returns_500(
        self, mock_provider_manager_get
    ):
        """test_provider_manager_update_fails_returns_500"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            delete_exc=Exception("mock_provider_manager_update_exception")
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.delete(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 500)

    @patch.object(ProviderManager, "get")
    def test_success_returns_200(self, mock_provider_manager_get):
        """test_success_returns_200"""

        mock_provider_manager_get.return_value = mocks.MockProviderManager(
            delete_result=mocks.MockResponse()
        )

        test_view = providers_views.ProviderRecordView()
        response = test_view.delete(
            self.mock_request,
            "mock_provider",
            f"{settings.ID_PROVIDER_PREFIXES[0]}/mock_record",
        )

        self.assertEqual(response.status_code, 200)
