""" Unit tests for core_linked_records_app.components.local_id.api
"""
from unittest import TestCase

from unittest.mock import patch

from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.components.local_id.models import LocalId
from core_main_app.commons import exceptions


class TestGetByName(TestCase):
    @patch.object(LocalId, "get_by_name")
    def test_get_by_name_failure_raises_api_error(self, mock_get_by_name):
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_api.get_by_name("mock_name")

    @patch.object(LocalId, "get_by_name")
    def test_returns_get_by_name_output(self, mock_get_by_name):
        expected_result = "mock_get_by_name"
        mock_get_by_name.return_value = expected_result

        self.assertEquals(local_id_api.get_by_name("mock_name"), expected_result)


class TestGetByClassAndId(TestCase):
    @patch.object(LocalId, "get_by_class_and_id")
    def test_get_by_class_and_id_failure_raises_api_error(
        self, mock_get_by_class_and_id
    ):
        mock_get_by_class_and_id.side_effect = Exception(
            "mock_get_by_class_and_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            local_id_api.get_by_class_and_id("class", "id")

    @patch.object(LocalId, "get_by_class_and_id")
    def test_returns_get_by_class_and_id_output(self, mock_get_by_class_and_id):
        expected_result = "mock_get_by_class_and_id"
        mock_get_by_class_and_id.return_value = expected_result

        self.assertEquals(
            local_id_api.get_by_class_and_id("class", "id"), expected_result
        )


class TestInsert(TestCase):
    def setUp(self) -> None:
        self.mock_local_id = LocalId(record_name="mock_record_name")

    @patch.object(LocalId, "upsert")
    def test_save_failure_raises_api_error(self, mock_save):
        mock_save.side_effect = Exception("mock_save_general_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_api.insert(self.mock_local_id)

    @patch.object(LocalId, "upsert")
    def test_returns_save_output(self, mock_save):
        expected_result = "mock_save"
        mock_save.return_value = expected_result

        self.assertEquals(local_id_api.insert(self.mock_local_id), expected_result)


class TestDelete(TestCase):
    def setUp(self) -> None:
        self.mock_local_id = LocalId(record_name="mock_record_name")

    @patch.object(LocalId, "delete")
    def test_delete_raises_api_error(self, mock_delete):
        mock_delete.side_effect = Exception("mock_delete_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_api.delete(self.mock_local_id)

    @patch.object(LocalId, "delete")
    def test_returns_delete_output(self, mock_delete):
        expected_result = "mock_delete"
        mock_delete.return_value = expected_result

        self.assertEquals(local_id_api.delete(self.mock_local_id), expected_result)
