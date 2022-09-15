""" Unit tests for core_linked_records_app.components.blob.watch
"""
import json
from unittest import TestCase
from unittest.mock import patch

from core_main_app.commons import exceptions
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.blob import watch as blob_watch
from core_linked_records_app.components.pid_settings import api as pid_settings_api

from tests import mocks


class TestSetBlobPid(TestCase):
    """Test Set Blob Pid"""

    def setUp(self):
        """setUp"""

        self.mock_document = mocks.MockDocument()

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(pid_settings_api, "get")
    def test_pid_setting_get_failure_raises_core_error(
        self, mock_get, mock_get_pid_for_blob
    ):
        """test_pid_setting_get_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.side_effect = Exception("mock_get_exception")

        with self.assertRaises(exceptions.CoreError):
            blob_watch.set_blob_pid(None, self.mock_document)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_reverse_failure_raises_core_error(
        self, mock_get, mock_reverse, mock_get_pid_for_blob
    ):
        """test_reverse_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.side_effect = Exception("mock_reverse_exception")

        with self.assertRaises(exceptions.CoreError):
            blob_watch.set_blob_pid(None, self.mock_document)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_watch, "send_post_request")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_send_post_request_failure_raises_core_error(
        self, mock_get, mock_reverse, mock_send_post_request, mock_get_pid_for_blob
    ):
        """test_send_post_request_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.return_value = "mock/reverse/url"
        mock_send_post_request.side_effect = Exception(
            "mock_send_post_request_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            blob_watch.set_blob_pid(None, self.mock_document)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_watch, "send_post_request")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_json_loads_failure_raises_core_error(
        self, mock_get, mock_reverse, mock_send_post_request, mock_get_pid_for_blob
    ):
        """test_json_loads_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.return_value = "mock/reverse/url"
        mock_send_post_request.return_value = "mock_not_json_return_value"

        with self.assertRaises(exceptions.CoreError):
            blob_watch.set_blob_pid(None, self.mock_document)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(blob_watch, "send_post_request")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_set_pid_for_blob_failure_raises_core_error(
        self,
        mock_get,
        mock_reverse,
        mock_send_post_request,
        mock_set_pid_for_blob,
        mock_get_pid_for_blob,
    ):
        """test_set_pid_for_blob_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.return_value = "mock/reverse/url"

        mock_pid_response = mocks.MockResponse()
        mock_pid_response.content = json.dumps({"url": "mock_pid_response_url"})
        mock_send_post_request.return_value = mock_pid_response
        mock_set_pid_for_blob.side_effect = Exception("mock_set_pid_for_blob_exception")

        with self.assertRaises(exceptions.CoreError):
            blob_watch.set_blob_pid(None, self.mock_document)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(pid_settings_api, "get")
    def test_auto_set_pid_false_does_not_assign_pid(
        self, mock_get, mock_set_pid_for_blob, mock_get_pid_for_blob
    ):
        """test_auto_set_pid_false_does_not_assign_pid"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_pid_settings = mocks.MockPidSettings()
        mock_pid_settings.auto_set_pid = False
        mock_get.return_value = mock_pid_settings

        blob_watch.set_blob_pid(None, self.mock_document)
        mock_set_pid_for_blob.assert_not_called()

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(blob_watch, "send_post_request")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_auto_set_pid_true_assign_pid(
        self,
        mock_get,
        mock_reverse,
        mock_send_post_request,
        mock_set_pid_for_blob,
        mock_get_pid_for_blob,
    ):
        """test_auto_set_pid_true_assign_pid"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.return_value = "mock/reverse/url"

        mock_pid_response = mocks.MockResponse()
        mock_pid_response.content = json.dumps({"url": "mock_pid_response_url"})
        mock_send_post_request.return_value = mock_pid_response
        mock_set_pid_for_blob.return_value = None

        blob_watch.set_blob_pid(None, self.mock_document)
        mock_set_pid_for_blob.assert_called_once()

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(pid_settings_api, "get")
    def test_auto_set_pid_false_returns_none(self, mock_get, mock_get_pid_for_blob):
        """test_auto_set_pid_false_returns_none"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_pid_settings = mocks.MockPidSettings()
        mock_pid_settings.auto_set_pid = False
        mock_get.return_value = mock_pid_settings

        result = blob_watch.set_blob_pid(None, self.mock_document)
        self.assertIsNone(result)

    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_api, "set_pid_for_blob")
    @patch.object(blob_watch, "send_post_request")
    @patch.object(blob_watch, "reverse")
    @patch.object(pid_settings_api, "get")
    def test_auto_set_pid_true_returns_none(
        self,
        mock_get,
        mock_reverse,
        mock_send_post_request,
        mock_set_pid_for_blob,
        mock_get_pid_for_blob,
    ):
        """test_auto_set_pid_true_returns_none"""

        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.return_value = mocks.MockPidSettings()
        mock_reverse.return_value = "mock/reverse/url"

        mock_pid_response = mocks.MockResponse()
        mock_pid_response.content = json.dumps({"url": "mock_pid_response_url"})
        mock_send_post_request.return_value = mock_pid_response
        mock_set_pid_for_blob.return_value = None

        result = blob_watch.set_blob_pid(None, self.mock_document)
        self.assertIsNone(result)

    @patch.object(pid_settings_api, "get")
    @patch.object(blob_api, "get_pid_for_blob")
    @patch.object(blob_api, "set_pid_for_blob")
    def test_pid_not_created_if_already_assigned(
        self, mock_set_pid_for_blob, mock_get_pid_for_blob, mock_settings_get
    ):
        """test_pid_not_created_if_already_assigned"""

        mock_get_pid_for_blob.return_value = "mock_pid"
        mock_settings_get.return_value = mocks.MockPidSettings()

        blob_watch.set_blob_pid(None, self.mock_document)
        self.assertFalse(mock_set_pid_for_blob.called)
