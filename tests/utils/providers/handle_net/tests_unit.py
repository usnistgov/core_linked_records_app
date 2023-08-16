""" Unit tests for core_linked_records_app.utils.providers.handle_net
"""
import json
from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app.utils.providers.handle_net import HandleNetSystem
from tests.mocks import MockResponse


class TestHandleNetSystemUpdateResponseContent(TestCase):
    """Test Handle Net System Update Response Content"""

    def test_returns_dict_with_message_key(self):
        """test_returns_dict_with_message_key"""

        pass

    def test_returns_dict_with_url_key(self):
        """test_returns_dict_with_url_key"""

        pass


class TestHandleNetSystemEncodeToken(TestCase):
    """Test Handle Net System Encode Token"""

    def test_returned_base64_encoding(self):
        """test_returned_base64_encoding"""

        pass


class TestHandleNetSystemGet(TestCase):
    """Test Handle Net System Get"""

    def test_record_url_called(self):
        """test_record_url_called"""

        pass

    def test_returns_dict_with_message_key(self):
        """test_returns_dict_with_message_key"""

        pass

    def test_returns_dict_with_url_key(self):
        """test_returns_dict_with_url_key"""

        pass


class TestHandleNetSystemCreate(TestCase):
    """Test Handle Net System Create"""

    def test_record_not_none_calls_existing_record_url(self):
        """test_record_not_none_calls_existing_record_url"""

        pass

    def test_record_not_none_returns_dict_with_message_key(self):
        """test_record_not_none_returns_dict_with_message_key"""

        pass

    def test_record_not_none_returns_dict_with_url_key(self):
        """test_record_not_none_returns_dict_with_url_key"""
        pass

    def test_record_none_calls_new_record_url(self):
        """test_record_none_calls_new_record_url"""

        pass

    def test_record_none_calls_update_method(self):
        """test_record_none_calls_update_method"""
        pass


class TestHandleNetSystemUpdate(TestCase):
    """Test Handle Net System Update"""

    def setUp(self) -> None:
        self.mock_handle_system = HandleNetSystem(
            "mock_provider_name",
            "mock_provider_lookup_url",
            "mock_provider_registration_url",
            "mock_username",
            "mock_password",
        )

    @patch(
        "core_linked_records_app.utils.providers.handle_net.send_put_request"
    )
    def test_send_put_request_on_record_url(self, mock_send_put_request):
        """test_send_put_request_on_record_url"""
        mock_record = "mock_record"
        mock_put_response = {"handle": "mock_handle", "responseCode": 000}
        mock_send_put_request.return_value = MockResponse(
            content=json.dumps(mock_put_response)
        )

        self.mock_handle_system.update(mock_record)
        mock_send_put_request.assert_called_with(
            f"{self.mock_handle_system.provider_registration_url}/"
            f"{self.mock_handle_system.registration_api}/{mock_record}?overwrite=true",
            self.mock_handle_system._generate_record_data(
                mock_record, include_handle=True
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {str(self.mock_handle_system.auth_token)}",
            },
        )

    def test_returns_dict_with_message_key(self):
        """test_returns_dict_with_message_key"""

        pass

    def test_returns_dict_with_url_key(self):
        """test_returns_dict_with_url_key"""

        pass


class TestHandleNetSystemDelete(TestCase):
    """Test Handle Net System Delete"""

    def test_send_delete_request_on_record_url(self):
        """test_send_delete_request_on_record_url"""

        pass

    def test_returns_dict_with_message_key(self):
        """test_returns_dict_with_message_key"""

        pass

    def test_returns_dict_with_url_key(self):
        """test_returns_dict_with_url_key"""

        pass
