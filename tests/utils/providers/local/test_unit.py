""" Unit tests for core_linked_records_app.utils.providers.local
"""
from unittest import TestCase


class TestLocalIdProviderEncodeToken(TestCase):
    """Test Local Id Provider Encode Token"""

    def test_returns_none(self):
        """test_returns_none"""

        pass


class TestLocalIdProviderIsIdAlreadyUsed(TestCase):
    """Test Local Id Provider Is Id Already Used"""

    def test_calls_get_method(self):
        """test_calls_get_method"""

        pass

    def test_returns_true_if_successful(self):
        """test_returns_true_if_successful"""

        pass

    def test_returns_false_if_failure(self):
        """test_returns_false_if_failure"""

        pass


class TestLocalIdProviderGet(TestCase):
    """Test Local Id Provider Get"""

    def test_non_existing_record_returns_404(self):
        """test_non_existing_record_returns_404"""

        pass

    def test_existing_record_returns_200(self):
        """test_existing_record_returns_200"""

        pass


class TestLocalIdProviderCreate(TestCase):
    """Test Local Id Provider Create"""

    def test_record_none_generate_new_record(self):
        """test_record_none_generate_new_record"""

        pass

    def test_non_unique_record_returns_409(self):
        """test_non_unique_record_returns_409"""

        pass

    def test_successful_creation_returns_201(self):
        """test_successful_creation_returns_201"""

        pass


class TestLocalIdProviderUpdate(TestCase):
    """Test Local Id Provider Update"""

    def test_record_in_response_key(self):
        """test_record_in_response_key"""

        pass

    def test_message_in_response_key(self):
        """test_message_in_response_key"""

        pass

    def test_url_in_response_key(self):
        """test_url_in_response_key"""

        pass


class TestLocalIdProviderDelete(TestCase):
    """Test Local Id Provider Delete"""

    def test_successful_delete_returns_200(self):
        """test_successful_delete_returns_200"""

        pass

    def test_non_existing_record_returns_404(self):
        """test_non_existing_record_returns_404"""

        pass
