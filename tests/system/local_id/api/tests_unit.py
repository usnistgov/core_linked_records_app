""" Unit tests for core_linked_records_app.system.local_id.api.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.system.local_id import (
    api as local_id_system_api,
)
from core_main_app.commons import exceptions


class TestGetByName(TestCase):
    """Unit tests for `get_by_name` function."""

    def setUp(self) -> None:
        """setUp"""
        self.kwargs = {
            "record_name": "mock_name",
        }

    @patch.object(LocalId, "get_by_name")
    def test_local_id_get_by_name_called(self, mock_get_by_name):
        """test_local_id_get_by_name_called"""
        local_id_system_api.get_by_name(**self.kwargs)
        mock_get_by_name.assert_called_with(self.kwargs["record_name"])

    @patch.object(LocalId, "get_by_name")
    def test_get_by_name_does_not_exist_raises_does_not_exist(
        self, mock_get_by_name
    ):
        """test_get_by_name_does_not_exist_raises_does_not_exist"""
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "mock_get_by_name_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            local_id_system_api.get_by_name(**self.kwargs)

    @patch.object(LocalId, "get_by_name")
    def test_get_by_name_exception_raises_api_error(self, mock_get_by_name):
        """test_get_by_name_exception_raises_api_error"""
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_system_api.get_by_name(**self.kwargs)

    @patch.object(LocalId, "get_by_name")
    def test_successful_execution_returns_local_id_get_by_name_value(
        self, mock_get_by_name
    ):
        """test_successful_execution_returns_local_id_get_by_name_value"""
        expected_value = MagicMock()
        mock_get_by_name.return_value = expected_value
        self.assertEqual(
            local_id_system_api.get_by_name(**self.kwargs), expected_value
        )


class TestGetByClassAndId(TestCase):
    """Unit tests for `get_by_class_and_id` function."""

    @patch.object(LocalId, "get_by_class_and_id")
    def test_get_by_class_and_id_does_not_exist_raises_does_not_exist(
        self, mock_get_by_class_and_id
    ):
        """test_get_by_class_and_id_failure_raises_api_error"""

        mock_get_by_class_and_id.side_effect = exceptions.DoesNotExist(
            "mock_get_by_class_and_id_exception"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            local_id_system_api.get_by_class_and_id("class", "id")

    @patch.object(LocalId, "get_by_class_and_id")
    def test_get_by_class_and_id_failure_raises_api_error(
        self, mock_get_by_class_and_id
    ):
        """test_get_by_class_and_id_failure_raises_api_error"""

        mock_get_by_class_and_id.side_effect = Exception(
            "mock_get_by_class_and_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            local_id_system_api.get_by_class_and_id("class", "id")

    @patch.object(LocalId, "get_by_class_and_id")
    def test_returns_get_by_class_and_id_output(
        self, mock_get_by_class_and_id
    ):
        """test_returns_get_by_class_and_id_output"""

        expected_result = "mock_get_by_class_and_id"
        mock_get_by_class_and_id.return_value = expected_result

        self.assertEqual(
            local_id_system_api.get_by_class_and_id("class", "id"),
            expected_result,
        )


class TestInsert(TestCase):
    """Test Insert"""

    def setUp(self) -> None:
        self.mock_local_id = LocalId(record_name="mock_record_name")

    @patch.object(LocalId, "upsert")
    def test_save_failure_raises_api_error(self, mock_save):
        """test_save_failure_raises_api_error"""

        mock_save.side_effect = Exception("mock_save_general_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_system_api.insert(self.mock_local_id)

    @patch.object(LocalId, "upsert")
    def test_returns_save_output(self, mock_save):
        """test_returns_save_output"""

        mock_save.return_value = None

        self.assertEqual(
            local_id_system_api.insert(self.mock_local_id), self.mock_local_id
        )


class TestDelete(TestCase):
    """Test Delete"""

    def setUp(self) -> None:
        self.mock_local_id = LocalId(record_name="mock_record_name")

    @patch.object(LocalId, "delete")
    def test_delete_raises_api_error(self, mock_delete):
        """test_delete_raises_api_error"""

        mock_delete.side_effect = Exception("mock_delete_exception")

        with self.assertRaises(exceptions.ApiError):
            local_id_system_api.delete(self.mock_local_id)

    @patch.object(LocalId, "delete")
    def test_returns_delete_output(self, mock_delete):
        """test_returns_delete_output"""

        expected_result = "mock_delete"
        mock_delete.return_value = expected_result

        self.assertEqual(
            local_id_system_api.delete(self.mock_local_id), expected_result
        )
