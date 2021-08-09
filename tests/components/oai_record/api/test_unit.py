""" Unit tests for core_linked_records_app.components.oai_record.api
"""
from unittest import TestCase

from unittest.mock import patch

from core_linked_records_app.components.oai_record import api as oai_record_api
from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_main_app.commons.exceptions import ApiError
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_data
from tests import mocks


class TestGetPidForData(TestCase):
    @patch.object(oai_record_data, "get_by_id")
    def test_get_by_id_failure_raises_api_error(self, mock_get_by_id):
        mock_get_by_id.side_effect = Exception("mock_get_by_id_exception")

        with self.assertRaises(ApiError):
            oai_record_api.get_pid_for_data("mock_id", mocks.MockRequest())

    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(oai_record_data, "get_by_id")
    def test_get_by_template_id_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template_id
    ):
        mock_get_by_id.return_value = mocks.MockData()
        mock_get_by_template_id.side_effect = Exception(
            "mock_get_by_template_id_exception"
        )

        with self.assertRaises(ApiError):
            oai_record_api.get_pid_for_data("mock_id", mocks.MockRequest())

    @patch.object(oai_record_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(oai_record_data, "get_by_id")
    def test_get_dict_value_from_key_list_failure_raises_api_error(
        self, mock_get_by_id, mock_get_by_template_id, mock_get_dict_value_from_key_list
    ):
        mock_get_by_id.return_value = mocks.MockData()
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.side_effect = Exception(
            "mock_get_dict_value_from_key_list_exception"
        )

        with self.assertRaises(ApiError):
            oai_record_api.get_pid_for_data("mock_id", mocks.MockRequest())

    @patch.object(oai_record_api, "get_dict_value_from_key_list")
    @patch.object(pid_xpath_api, "get_by_template_id")
    @patch.object(oai_record_data, "get_by_id")
    def test_returns_get_dict_value_from_key_list(
        self, mock_get_by_id, mock_get_by_template_id, mock_get_dict_value_from_key_list
    ):
        expected_result = "mock_get_pid_for_data"
        mock_get_by_id.return_value = mocks.MockData()
        mock_get_by_template_id.return_value = mocks.MockPidXpath()
        mock_get_dict_value_from_key_list.return_value = expected_result

        self.assertEquals(
            oai_record_api.get_pid_for_data("mock_id", mocks.MockRequest()),
            expected_result,
        )
