""" Unit tests for core_linked_records_app.rest.pid.views
"""
import json
from unittest import TestCase
from unittest.mock import patch

from core_explore_common_app.components.query import api as query_api
from core_federated_search_app.components.instance import (
    api as instance_api,
)
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.data import api as data_api
from core_linked_records_app.rest.pid import views as pid_views
from tests import mocks


class TestRetrieveDataPidGet(TestCase):
    """Test Retrieve Data Pid Get"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()
        self.mock_request.GET = dict()

    @patch.object(data_api, "get_pid_for_data")
    def test_data_api_get_pid_for_data_fails_returns_500(self, mock_get_pid_for_data):
        """test_data_api_get_pid_for_data_fails_returns_500"""

        self.mock_request.GET["data_id"] = "mock_data_id"
        mock_get_pid_for_data.side_effect = Exception("mock_get_pid_for_data_exception")

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(data_api, "get_pid_for_data")
    def test_data_api_success_returns_200(self, mock_get_pid_for_data):
        """test_data_api_success_returns_200"""

        self.mock_request.GET["data_id"] = "mock_data_id"
        mock_get_pid_for_data.return_value = "mock_data_id"

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 200)

    # FIXME cannot import oai_pmh_harvester in INSTALLED_APPS
    # def test_oai_record_api_get_pid_for_data_fails_returns_500(self):
    #     pass
    #
    # def test_oai_record_api_success_returns_200(self):
    #     pass

    @patch.object(instance_api, "get_by_name")
    def test_instance_api_get_by_name_fails_returns_500(self, mock_get_by_name):
        """test_instance_api_get_by_name_fails_returns_500"""

        self.mock_request.GET["fede_data_id"] = "mock_data_id"
        self.mock_request.GET["fede_origin"] = "mock_origin&param=mock_param"
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "oauth2_get_request")
    @patch.object(instance_api, "get_by_name")
    def test_oauth2_get_request_fails_returns_500(
        self, mock_get_by_name, mock_oauth2_get_request
    ):
        """test_oauth2_get_request_fails_returns_500"""

        self.mock_request.GET["fede_data_id"] = "mock_data_id"
        self.mock_request.GET["fede_origin"] = "mock_origin&param=mock_param"
        mock_get_by_name.return_value = mocks.MockInstance()
        mock_oauth2_get_request.side_effect = Exception(
            "mock_oauth2_get_request_exception"
        )

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "oauth2_get_request")
    @patch.object(instance_api, "get_by_name")
    def test_fede_success_returns_200(self, mock_get_by_name, mock_oauth2_get_request):
        """test_fede_success_returns_200"""

        self.mock_request.GET["fede_data_id"] = "mock_data_id"
        self.mock_request.GET["fede_origin"] = "mock_origin&param=mock_param"
        mock_get_by_name.return_value = mocks.MockInstance()
        mock_oauth2_get_request.return_value = mocks.MockResponse(
            text=json.dumps({"key": "mock_response_text"})
        )

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 200)

    def test_incorrect_params_returns_400(self):
        """test_incorrect_params_returns_400"""

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 400)


class TestRetrieveBlobPidGet(TestCase):
    """Test Retrieve Blob Pid Get"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()
        self.mock_request.GET = dict()

    @patch.object(blob_api, "get_pid_for_blob")
    def test_get_pid_for_blob_fails_returns_500(self, mock_get_pid_for_blob):
        """test_get_pid_for_blob_fails_returns_500"""

        self.mock_request.GET["blob_id"] = "mock_blob_id"
        mock_get_pid_for_blob.side_effect = Exception("mock_get_pid_for_blob_exception")

        test_view = pid_views.RetrieveBlobPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(blob_api, "get_pid_for_blob")
    def test_success_returns_200(self, mock_get_pid_for_blob):
        """test_success_returns_200"""

        self.mock_request.GET["blob_id"] = "mock_blob_id"
        mock_get_pid_for_blob.return_value = mocks.MockLocalId()

        test_view = pid_views.RetrieveBlobPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 200)

    def test_incorrect_params_returns_400(self):
        """test_incorrect_params_returns_400"""

        test_view = pid_views.RetrieveBlobPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 400)


class TestRetrieveListPidPost(TestCase):
    """Test Retrieve List Pid Post"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest(POST={"query_id": "mock_query_id"})

    @patch.object(query_api, "get_by_id")
    def test_get_by_id_fails_returns_500(self, mock_get_by_id):
        """test_get_by_id_fails_returns_500"""

        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(query_api, "get_by_id")
    def test_data_source_no_pid_url_capabilities_returns_500(self, mock_get_by_id):
        """test_data_source_no_pid_url_capabilities_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[mocks.MockDataSource()]
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "send_get_request")
    @patch.object(query_api, "get_by_id")
    def test_send_get_request_fails_returns_500(
        self, mock_get_by_id, mock_send_get_request
    ):
        """test_send_get_request_fails_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                mocks.MockDataSource(
                    capabilities={"url_pid": "mock_url_pid"},
                    authentication=mocks.MockAuthentication(type="session"),
                )
            ]
        )
        mock_send_get_request.side_effect = Exception("mock_send_get_request_exception")

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_oauth2_post_request_fails_returns_500(
        self, mock_get_by_id, mock_oauth2_post_request
    ):
        """test_oauth2_post_request_fails_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                mocks.MockDataSource(
                    capabilities={"url_pid": "mock_url_pid"},
                    authentication=mocks.MockAuthentication(
                        type="oauth2",
                        params={"access_token": "mock_access_token"},
                    ),
                )
            ]
        )
        mock_oauth2_post_request.side_effect = Exception(
            "mock_oauth2_post_request_exception"
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(query_api, "get_by_id")
    def test_unknown_auth_returns_500(self, mock_get_by_id):
        """test_unknown_auth_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                mocks.MockDataSource(
                    authentication=mocks.MockAuthentication(type="mock_auth")
                )
            ]
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_status_200_returns_200(self, mock_get_by_id, mock_oauth2_post_request):
        """test_status_200_returns_200"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options=dict(),
                    order_by_field="",
                    capabilities={"url_pid": "mock_url_pid"},
                    authentication=dict(
                        auth_type="oauth2",
                        params={"access_token": "mock_access_token"},
                    ),
                )
            ]
        )
        mock_oauth2_post_request.return_value = mocks.MockResponse(json_data=list())

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 200)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_status_400_returns_400(self, mock_get_by_id, mock_oauth2_post_request):
        """test_status_400_returns_400"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options=dict(),
                    order_by_field="",
                    capabilities={"url_pid": "mock_url_pid"},
                    authentication=dict(
                        auth_type="oauth2",
                        params={"access_token": "mock_access_token"},
                    ),
                )
            ],
        )
        mock_oauth2_post_request.return_value = mocks.MockResponse(status_code=400)

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 400)
