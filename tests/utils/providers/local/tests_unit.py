""" Unit tests for core_linked_records_app.utils.providers.local
"""
import json
from unittest import TestCase
from unittest.mock import patch

from rest_framework import status

from core_linked_records_app.utils.providers.local import LocalIdProvider
from core_main_app.commons import exceptions
from tests.mocks import MockResponse, MockLocalId


class TestLocalIdProviderIsIdAlreadyUsed(TestCase):
    """Test Local Id Provider Is Id Already Used"""

    def setUp(self) -> None:
        self.provider = LocalIdProvider("mock_provider")

    @patch("core_linked_records_app.utils.providers.local.LocalIdProvider.get")
    def test_calls_get_method(self, mock_get):
        """test_calls_get_method"""
        mock_get_value = MockResponse()
        mock_get_value.content = json.dumps({"message": "mock_message"})
        mock_get.return_value = mock_get_value

        self.provider.is_id_already_used("mock_record")
        mock_get.assert_called()

    @patch("core_linked_records_app.utils.providers.local.LocalIdProvider.get")
    def test_returns_true_if_successful(self, mock_get):
        """test_returns_true_if_successful"""
        mock_get_value = MockResponse()
        mock_get_value.content = json.dumps(
            {"message": self.provider.messages["success"]}
        )
        mock_get.return_value = mock_get_value

        self.assertTrue(self.provider.is_id_already_used("mock_record"))

    @patch("core_linked_records_app.utils.providers.local.LocalIdProvider.get")
    def test_returns_false_if_failure(self, mock_get):
        """test_returns_false_if_failure"""
        mock_get_value = MockResponse()
        mock_get_value.content = json.dumps(
            {"message": self.provider.messages["not_found"]}
        )
        mock_get.return_value = mock_get_value

        self.assertFalse(self.provider.is_id_already_used("mock_record"))


class TestLocalIdProviderGet(TestCase):
    """Test Local Id Provider Get"""

    def setUp(self) -> None:
        self.provider = LocalIdProvider("mock_provider")
        self.record = "mock_record"

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_non_existing_record_returns_404(self, mock_get_by_name):
        """test_non_existing_record_returns_404"""
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "mock_does_not_exists"
        )
        self.assertEqual(
            self.provider.get(self.record).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_non_existing_record_returns_correct_content(
        self, mock_get_by_name
    ):
        """test_non_existing_record_returns_correct_content"""
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "mock_does_not_exists"
        )
        self.assertEqual(
            json.loads(self.provider.get(self.record).content),
            {
                "message": self.provider.messages["not_found"],
                "record": self.record,
                "url": f"{self.provider.provider_lookup_url}/{self.record}",
            },
        )

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_existing_record_returns_200(self, mock_get_by_name):
        """test_existing_record_returns_200"""
        mock_get_by_name.return_value = None
        self.assertEqual(
            self.provider.get(self.record).status_code, status.HTTP_200_OK
        )

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_existing_record_returns_correct_content(self, mock_get_by_name):
        """test_existing_record_returns_correct_content"""
        mock_get_by_name.return_value = None
        self.assertEqual(
            json.loads(self.provider.get(self.record).content),
            {
                "message": self.provider.messages["success"],
                "record": self.record,
                "url": f"{self.provider.provider_lookup_url}/{self.record}",
            },
        )


class TestLocalIdProviderCreate(TestCase):
    """Test Local Id Provider Create"""

    def setUp(self) -> None:
        self.provider = LocalIdProvider("mock_provider")
        self.prefix = "mock_prefix"
        self.record = "mock_record"

    @patch("core_linked_records_app.system.local_id.api.insert")
    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider.is_id_already_used"
    )
    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider._generate_id"
    )
    def test_record_none_generate_new_record(
        self, mock_generate_id, mock_is_id_already_used, mock_localid_insert
    ):
        """test_record_none_generate_new_record"""
        mock_generate_id.return_value = self.record
        mock_is_id_already_used.return_value = False
        mock_localid_insert.return_value = None
        self.provider.create(self.prefix)

        self.assertTrue(mock_generate_id.called)
        self.assertTrue(mock_is_id_already_used.called)

    @patch("core_linked_records_app.system.local_id.api.insert")
    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider.is_id_already_used"
    )
    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider._generate_id"
    )
    def test_record_none_ensure_new_record_is_unique(
        self, mock_generate_id, mock_is_id_already_used, mock_localid_insert
    ):
        """test_record_none_checks_new_record_is_unique"""
        mock_generate_id.return_value = self.record
        mock_is_id_already_used.side_effect = [True, False]
        mock_localid_insert.return_value = None
        self.provider.create(self.prefix)

        self.assertEqual(mock_generate_id.call_count, 2)
        self.assertEqual(mock_is_id_already_used.call_count, 2)

    @patch("core_linked_records_app.system.local_id.api.insert")
    def test_non_unique_record_returns_409(self, mock_localid_insert):
        """test_non_unique_record_returns_409"""
        mock_localid_insert.side_effect = exceptions.NotUniqueError(
            "mock_not_unique_error"
        )
        response = self.provider.create(self.prefix, self.record)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch("core_linked_records_app.system.local_id.api.insert")
    def test_non_unique_record_returns_correct_content(
        self, mock_localid_insert
    ):
        """test_non_unique_record_returns_correct_content"""
        mock_localid_insert.side_effect = exceptions.NotUniqueError(
            "mock_not_unique_error"
        )
        response = self.provider.create(self.prefix, self.record)

        self.assertEqual(
            json.loads(response.content),
            {
                "message": self.provider.messages["already_exist"],
                "record": f"{self.prefix}/{self.record}",
                "url": f"{self.provider.provider_lookup_url}/{self.prefix}/{self.record}",
            },
        )

    @patch("core_linked_records_app.system.local_id.api.insert")
    def test_successful_creation_returns_201(self, mock_localid_insert):
        """test_successful_creation_returns_201"""
        mock_localid_insert.return_value = None
        response = self.provider.create(self.prefix, self.record)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("core_linked_records_app.system.local_id.api.insert")
    def test_successful_creation_returns_correct_content(
        self, mock_localid_insert
    ):
        """test_successful_creation_returns_correct_content"""
        mock_localid_insert.return_value = None
        response = self.provider.create(self.prefix, self.record)

        self.assertEqual(
            json.loads(response.content),
            {
                "message": self.provider.messages["success"],
                "record": f"{self.prefix}/{self.record}",
                "url": f"{self.provider.provider_lookup_url}/{self.prefix}/{self.record}",
            },
        )


class TestLocalIdProviderUpdate(TestCase):
    """Test Local Id Provider Update"""

    def setUp(self) -> None:
        self.provider = LocalIdProvider("mock_provider")
        self.record = "mock_record"

    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider.create"
    )
    def test_create_is_called(self, mock_create):
        """test_create_is_called"""
        mock_create.return_value = None
        self.provider.update(self.record)

        self.assertTrue(mock_create.called)

    @patch(
        "core_linked_records_app.utils.providers.local.LocalIdProvider.create"
    )
    def test_returns_correct_content(self, mock_create):
        """test_returns_correct_content"""
        mock_create.return_value = None
        response = self.provider.update(self.record)

        self.assertEqual(
            json.loads(response.content),
            {
                "record": self.record,
                "message": self.provider.messages["success"],
                "url": f"{self.provider.provider_lookup_url}/{self.record}",
            },
        )


class TestLocalIdProviderDelete(TestCase):
    """Test Local Id Provider Delete"""

    def setUp(self) -> None:
        self.provider = LocalIdProvider("mock_provider")
        self.record = "mock_record"

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_delete_is_called(self, mock_get_by_name):
        """test_successful_delete_returns_200"""
        mock_local_id = MockLocalId()
        mock_get_by_name.return_value = mock_local_id

        self.provider.delete(self.record)
        self.assertTrue(mock_local_id.delete.called)

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_successful_delete_returns_200(self, mock_get_by_name):
        """test_successful_delete_returns_200"""
        mock_local_id = MockLocalId()
        mock_get_by_name.return_value = mock_local_id

        response = self.provider.delete(self.record)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_successful_delete_returns_correct_content(self, mock_get_by_name):
        """test_successful_delete_returns_correct_content"""
        mock_local_id = MockLocalId()
        mock_get_by_name.return_value = mock_local_id

        response = self.provider.delete(self.record)
        self.assertEqual(
            json.loads(response.content),
            {
                "record": self.record,
                "message": self.provider.messages["success"],
                "url": f"{self.provider.provider_lookup_url}/{self.record}",
            },
        )

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_non_existing_record_returns_404(self, mock_get_by_name):
        """test_non_existing_record_returns_404"""
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "mock_does_not_exist"
        )

        response = self.provider.delete(self.record)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("core_linked_records_app.system.local_id.api.get_by_name")
    def test_non_existing_record_returns_correct_content(
        self, mock_get_by_name
    ):
        """test_non_existing_record_returns_correct_content"""
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "mock_does_not_exist"
        )

        response = self.provider.delete(self.record)
        self.assertEqual(
            json.loads(response.content),
            {
                "record": self.record,
                "message": self.provider.messages["not_found"],
                "url": f"{self.provider.provider_lookup_url}/{self.record}",
            },
        )
