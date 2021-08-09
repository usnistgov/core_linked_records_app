""" Unit tests for core_linked_records_app.components.pid_xpath.api
"""
from unittest import TestCase

from unittest.mock import patch

from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import (
    api as template_api,
)
from tests import mocks


class TestGetByTemplateId(TestCase):
    def setUp(self) -> None:
        self.mock_template_id = "mock_template_id"
        self.kwargs = {
            "template_id": self.mock_template_id,
            "request": mocks.MockRequest(),
        }

    @patch.object(template_api, "get_all")
    def test_get_all_template_failure_raises_api_error(self, mock_get_all):
        mock_get_all.side_effect = Exception("mock_get_all_exception")

        with self.assertRaises(ApiError):
            pid_xpath_api.get_by_template_id(**self.kwargs)

    @patch.object(template_api, "get_all")
    def test_template_id_not_accessible_raises_acl_error(self, mock_get_all):
        mock_get_all.return_value = []

        with self.assertRaises(AccessControlError):
            pid_xpath_api.get_by_template_id(**self.kwargs)

    @patch.object(PidXpath, "get_by_template_id")
    @patch.object(template_api, "get_all")
    def test_get_by_template_id_failure_raises_api_error(
        self, mock_get_all, mock_get_by_template_id
    ):
        mock_template = mocks.MockDocument()
        mock_template.pk = self.mock_template_id
        mock_get_all.return_value = [mock_template]
        mock_get_by_template_id.side_effect = Exception(
            "mock_get_by_template_id_exception"
        )

        with self.assertRaises(ApiError):
            pid_xpath_api.get_by_template_id(**self.kwargs)

    @patch.object(PidXpath, "__init__")
    @patch.object(PidXpath, "get_by_template_id")
    @patch.object(template_api, "get_all")
    def test_pid_xpath_init_failure_raises_api_error(
        self, mock_get_all, mock_get_by_template_id, mock_pid_xpath
    ):
        mock_template = mocks.MockDocument()
        mock_template.pk = self.mock_template_id
        mock_get_all.return_value = [mock_template]
        mock_get_by_template_id.return_value = None
        mock_pid_xpath.side_effect = Exception("mock_pid_xpath_exception")

        with self.assertRaises(ApiError):
            pid_xpath_api.get_by_template_id(**self.kwargs)

    @patch.object(PidXpath, "__init__")
    @patch.object(PidXpath, "get_by_template_id")
    @patch.object(template_api, "get_all")
    def test_returns_new_pid_xpath_if_not_exists(
        self, mock_get_all, mock_get_by_template_id, mock_pid_xpath
    ):
        expected_result = "mock_pid_xpath_object"
        mock_template = mocks.MockDocument()
        mock_template.pk = self.mock_template_id
        mock_get_all.return_value = [mock_template]
        mock_get_by_template_id.return_value = expected_result

        self.assertEquals(
            pid_xpath_api.get_by_template_id(**self.kwargs), expected_result
        )

    @patch.object(PidXpath, "__new__")
    @patch.object(PidXpath, "get_by_template_id")
    @patch.object(template_api, "get_all")
    def test_returns_pid_xpath_if_exists(
        self, mock_get_all, mock_get_by_template_id, mock_pid_xpath
    ):
        expected_result = "mock_pid_xpath"
        mock_template = mocks.MockDocument()
        mock_template.pk = self.mock_template_id
        mock_get_all.return_value = [mock_template]
        mock_get_by_template_id.return_value = None
        mock_pid_xpath.return_value = expected_result

        self.assertEquals(
            pid_xpath_api.get_by_template_id(**self.kwargs), expected_result
        )


class TestGetAll(TestCase):
    @patch.object(template_api, "get_all")
    def test_template_api_get_all_failure_raises_api_error(self, mock_get_all):
        mock_get_all.side_effect = Exception("mock_get_all_exception")

        with self.assertRaises(ApiError):
            pid_xpath_api.get_all(mocks.MockRequest())

    @patch.object(PidXpath, "get_all_by_template_list")
    @patch.object(template_api, "get_all")
    def test_get_all_by_template_list_failure_raises_api_error(
        self, mock_get_all, mock_get_all_by_template_list
    ):
        mock_get_all.return_value = []
        mock_get_all_by_template_list.side_effect = Exception("mock_get_all_exception")

        with self.assertRaises(ApiError):
            pid_xpath_api.get_all(mocks.MockRequest())

    @patch.object(PidXpath, "get_all_by_template_list")
    @patch.object(template_api, "get_all")
    def test_returns_get_all_by_template_list_output(
        self, mock_get_all, mock_get_all_by_template_list
    ):
        expected_result = "mock_get_all_by_template_list"
        mock_get_all.return_value = []
        mock_get_all_by_template_list.return_value = expected_result

        self.assertEquals(pid_xpath_api.get_all(mocks.MockRequest()), expected_result)
