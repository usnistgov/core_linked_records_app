""" Unit tests for core_linked_records_app.utils.providers.local
"""
from unittest import TestCase


class TestLocalIdProviderEncodeToken(TestCase):
    def test_returns_none(self):
        pass


class TestLocalIdProviderIsIdAlreadyUsed(TestCase):
    def test_calls_get_method(self):
        pass

    def test_returns_true_if_successful(self):
        pass

    def test_returns_false_if_failure(self):
        pass


class TestLocalIdProviderGet(TestCase):
    def test_non_existing_record_returns_404(self):
        pass

    def test_existing_record_returns_200(self):
        pass


class TestLocalIdProviderCreate(TestCase):
    def test_record_none_generate_new_record(self):
        pass

    def test_non_unique_record_returns_409(self):
        pass

    def test_successful_creation_returns_201(self):
        pass


class TestLocalIdProviderUpdate(TestCase):
    def test_record_in_response_key(self):
        pass

    def test_message_in_response_key(self):
        pass

    def test_url_in_response_key(self):
        pass


class TestLocalIdProviderDelete(TestCase):
    def test_successful_delete_returns_200(self):
        pass

    def test_non_existing_record_returns_404(self):
        pass
