""" Unit tests for core_linked_records_app.rest.pid.views
"""
import json
from unittest import TestCase
from unittest.mock import patch

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.utils.oaipmh import oaipmh as oaipmh_utils
from core_explore_common_app.utils.query import query as query_utils
from core_federated_search_app.components.instance import (
    api as instance_api,
)
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.data import api as data_api
from core_linked_records_app.components.oai_record import (
    api as oai_record_api,
)
from core_linked_records_app.rest.pid import views as pid_views
from tests import mocks


class TestRetrieveDataPidGet(TestCase):
    """Test Retrieve Data Pid Get"""

    def setUp(self) -> None:
        self.mock_request = mocks.MockRequest()
        self.mock_request.GET = {}

    @patch.object(data_api, "get_pid_for_data")
    def test_data_api_get_pid_for_data_fails_returns_500(
        self, mock_get_pid_for_data
    ):
        """test_data_api_get_pid_for_data_fails_returns_500"""

        self.mock_request.GET["data_id"] = "mock_data_id"
        mock_get_pid_for_data.side_effect = Exception(
            "mock_get_pid_for_data_exception"
        )

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

    @patch.object(oai_record_api, "get_pid_for_data")
    def test_oai_record_api_get_pid_for_data_fails_returns_500(
        self, mock_get_pid_for_data
    ):
        """test_oai_record_api_get_pid_for_data_fails_returns_500"""
        self.mock_request.GET["oai_data_id"] = "mock_data_id"
        mock_get_pid_for_data.side_effect = Exception(
            "mock_get_pid_for_data_exception"
        )

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(oai_record_api, "get_pid_for_data")
    def test_oai_record_api_success_returns_200(self, mock_get_pid_for_data):
        """test_oai_record_api_success_returns_200"""
        self.mock_request.GET["oai_data_id"] = "mock_data_id"
        mock_get_pid_for_data.return_value = "mock_data_id"

        test_view = pid_views.RetrieveDataPIDView()
        response = test_view.get(self.mock_request)

        self.assertEqual(response.status_code, 200)

    @patch.object(instance_api, "get_by_name")
    def test_instance_api_get_by_name_fails_returns_500(
        self, mock_get_by_name
    ):
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
    def test_fede_success_returns_200(
        self, mock_get_by_name, mock_oauth2_get_request
    ):
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
        self.mock_request.GET = {}

    @patch.object(blob_api, "get_pid_for_blob")
    def test_get_pid_for_blob_fails_returns_500(self, mock_get_pid_for_blob):
        """test_get_pid_for_blob_fails_returns_500"""

        self.mock_request.GET["blob_id"] = "mock_blob_id"
        mock_get_pid_for_blob.side_effect = Exception(
            "mock_get_pid_for_blob_exception"
        )

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
        self.mock_request = mocks.MockRequest(
            data={"query_id": "mock_query_id"}
        )

    @patch.object(query_api, "get_by_id")
    def test_get_by_id_fails_returns_500(self, mock_get_by_id):
        """test_get_by_id_fails_returns_500"""

        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(query_api, "get_by_id")
    def test_data_source_invalid_returns_500(self, mock_get_by_id):
        """test_data_source_invalid_returns_500"""
        mock_get_by_id.return_value = mocks.MockQuery(data_sources=[])

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(query_api, "get_by_id")
    def test_unknown_datasource_authtype_returns_400(self, mock_get_by_id):
        """test_unknown_auth_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="invalid_auth_type",
                    ),
                )
            ]
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 400)

    @patch.object(query_api, "get_by_id")
    def test_invalid_datasource_auth_type_returns_500(self, mock_get_by_id):
        """test_unknown_auth_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication={},
                )
            ]
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(oaipmh_utils, "is_oai_data_source")
    @patch.object(query_utils, "is_local_data_source")
    @patch.object(query_api, "get_by_id")
    def test_invalid_session_datasource_returns_500(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
    ):
        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="session",
                    ),
                )
            ]
        )
        mock_is_local_data_source.return_value = False
        mock_is_oai_data_source.return_value = False

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 500)

    @patch.object(pid_views, "execute_local_pid_query")
    @patch.object(oaipmh_utils, "is_oai_data_source")
    @patch.object(query_utils, "is_local_data_source")
    @patch.object(query_api, "get_by_id")
    def test_local_datasource_returns_200(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
        mock_execute_local_pid_query,
    ):
        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="session",
                    ),
                )
            ]
        )
        mock_is_local_data_source.return_value = True
        mock_is_oai_data_source.return_value = False
        mock_execute_local_pid_query.return_value = []

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 200)

    @patch.object(pid_views, "execute_local_pid_query")
    @patch.object(oaipmh_utils, "is_oai_data_source")
    @patch.object(query_utils, "is_local_data_source")
    @patch.object(query_api, "get_by_id")
    def test_local_datasource_returns_local_pid_query(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
        mock_execute_local_pid_query,
    ):
        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="session",
                    ),
                )
            ]
        )
        mock_is_local_data_source.return_value = True
        mock_is_oai_data_source.return_value = False

        expected_result = ["mock_pid" for _ in range(5)]
        mock_execute_local_pid_query.return_value = expected_result

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)
        result = response.data["pids"]

        self.assertEqual(result, expected_result)

    @patch.object(pid_views, "execute_oaipmh_pid_query")
    @patch.object(oaipmh_utils, "is_oai_data_source")
    @patch.object(query_utils, "is_local_data_source")
    @patch.object(query_api, "get_by_id")
    def test_oaipmh_datasource_returns_200(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
        mock_execute_oaipmh_pid_query,
    ):
        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="session",
                    ),
                )
            ]
        )
        mock_is_local_data_source.return_value = False
        mock_is_oai_data_source.return_value = True
        mock_execute_oaipmh_pid_query.return_value = []

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 200)

    @patch.object(pid_views, "execute_oaipmh_pid_query")
    @patch.object(oaipmh_utils, "is_oai_data_source")
    @patch.object(query_utils, "is_local_data_source")
    @patch.object(query_api, "get_by_id")
    def test_oaipmh_datasource_returns_oaipmh_pid_query(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
        mock_execute_oaipmh_pid_query,
    ):
        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={},
                    authentication=dict(
                        auth_type="session",
                    ),
                )
            ]
        )
        mock_is_local_data_source.return_value = False
        mock_is_oai_data_source.return_value = True
        expected_result = ["mock_pid" for _ in range(5)]
        mock_execute_oaipmh_pid_query.return_value = expected_result

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)
        result = response.data["pids"]

        self.assertEqual(result, expected_result)

    # FIXME need federation fixing first
    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_oauth2_post_request_fails_returns_500(
        self, mock_get_by_id, mock_oauth2_post_request
    ):
        """test_oauth2_post_request_fails_returns_500"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={"query_pid": "mock_url_pid"},
                    authentication=dict(
                        auth_type="oauth2",
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

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_status_200_returns_200(
        self, mock_get_by_id, mock_oauth2_post_request
    ):
        """test_status_200_returns_200"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={"query_pid": "mock_url_pid"},
                    authentication=dict(
                        auth_type="oauth2",
                        params={"access_token": "mock_access_token"},
                    ),
                )
            ]
        )
        mock_oauth2_post_request.return_value = mocks.MockResponse(
            json_data={"pids": []}
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 200)

    @patch.object(pid_views, "oauth2_post_request")
    @patch.object(query_api, "get_by_id")
    def test_status_400_returns_400(
        self, mock_get_by_id, mock_oauth2_post_request
    ):
        """test_status_400_returns_400"""

        mock_get_by_id.return_value = mocks.MockQuery(
            data_sources=[
                dict(
                    query_options={},
                    order_by_field="",
                    capabilities={"query_pid": "mock_url_pid"},
                    authentication=dict(
                        auth_type="oauth2",
                        params={"access_token": "mock_access_token"},
                    ),
                )
            ],
        )
        mock_oauth2_post_request.return_value = mocks.MockResponse(
            status_code=400
        )

        test_view = pid_views.RetrieveListPIDView()
        response = test_view.post(self.mock_request)

        self.assertEqual(response.status_code, 400)
