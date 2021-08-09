""" Unit tests for core_linked_records_app.utils.providers.handle_net
"""
from unittest import TestCase


class TestHandleNetSystemUpdateResponseContent(TestCase):
    def test_returns_dict_with_message_key(self):
        pass

    def test_returns_dict_with_url_key(self):
        pass


class TestHandleNetSystemEncodeToken(TestCase):
    def test_returned_base64_encoding(self):
        pass


class TestHandleNetSystemGet(TestCase):
    def test_record_url_called(self):
        pass

    def test_returns_dict_with_message_key(self):
        pass

    def test_returns_dict_with_url_key(self):
        pass


class TestHandleNetSystemCreate(TestCase):
    def test_record_not_none_calls_existing_record_url(self):
        pass

    def test_record_not_none_returns_dict_with_message_key(self):
        pass

    def test_record_not_none_returns_dict_with_url_key(self):
        pass

    def test_record_none_calls_new_record_url(self):
        pass

    def test_record_none_calls_update_method(self):
        pass


class TestHandleNetSystemUpdate(TestCase):
    def test_send_put_request_on_record_url(self):
        pass

    def test_returns_dict_with_message_key(self):
        pass

    def test_returns_dict_with_url_key(self):
        pass


class TestHandleNetSystemDelete(TestCase):
    def test_send_delete_request_on_record_url(self):
        pass

    def test_returns_dict_with_message_key(self):
        pass

    def test_returns_dict_with_url_key(self):
        pass
