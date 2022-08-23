""" Unit tests for core_linked_records_app.components.local_id.models
"""
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from core_main_app.commons import exceptions
from core_linked_records_app.components.local_id.models import LocalId


class TestGetByName(TestCase):
    """Test Get By Name"""

    @patch.object(LocalId, "objects")
    def test_local_id_get_does_not_exist_raises_does_not_exist_error(
        self, mock_objects
    ):
        """test_local_id_get_does_not_exist_raises_does_not_exist_error"""

        mock_objects.get.side_effect = ObjectDoesNotExist(
            "mock_objects_get_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            LocalId.get_by_name("mock_record_name")

    @patch.object(LocalId, "objects")
    def test_local_id_get_failure_raises_model_error(self, mock_objects):
        """test_local_id_get_failure_raises_model_error"""

        mock_objects.get.side_effect = Exception("mock_objects_get_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.get_by_name("mock_record_name")

    @patch.object(LocalId, "objects")
    def test_returns_local_id_get_output(self, mock_objects):
        """test_returns_local_id_get_output"""

        expected_result = "mock_get_by_name"
        mock_objects.get.return_value = expected_result

        self.assertEqual(LocalId.get_by_name("mock_record_name"), expected_result)


class TestGetByClassAndId(TestCase):
    """Test Get By Class And Id"""

    @patch.object(LocalId, "objects")
    def test_local_id_get_does_not_exist_raises_does_not_exist_error(
        self, mock_objects
    ):
        """test_local_id_get_does_not_exist_raises_does_not_exist_error"""

        mock_objects.get.side_effect = ObjectDoesNotExist(
            "mock_objects_get_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id")

    @patch.object(LocalId, "objects")
    def test_local_id_get_failure_raises_model_error(self, mock_objects):
        """test_local_id_get_failure_raises_model_error"""

        mock_objects.get.side_effect = Exception("mock_objects_get_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id")

    @patch.object(LocalId, "objects")
    def test_returns_local_id_get_output(self, mock_objects):
        """test_returns_local_id_get_output"""

        expected_result = "mock_get_by_name"
        mock_objects.get.return_value = expected_result

        self.assertEqual(
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id"),
            expected_result,
        )


class TestUpdate(TestCase):
    """Test Update"""

    def setUp(self):
        """setUp"""

        self.mock_local_id = LocalId()

    @patch.object(LocalId, "save")
    def test_local_id_save_not_unique_error_raises_not_unique_error(self, mock_save):
        """test_local_id_save_not_unique_error_raises_not_unique_error"""

        mock_save.side_effect = IntegrityError("mock_save_not_unique_error")

        with self.assertRaises(exceptions.NotUniqueError):
            LocalId.upsert(self.mock_local_id)

    @patch.object(LocalId, "save")
    def test_local_id_save_failure_raises_model_error(self, mock_save):
        """test_local_id_save_failure_raises_model_error"""

        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.upsert(self.mock_local_id)

    @patch.object(LocalId, "save")
    def test_returns_local_id_get_output(self, mock_save):
        """test_returns_local_id_get_output"""

        mock_save.return_value = None

        self.assertEqual(
            LocalId.upsert(self.mock_local_id),
            self.mock_local_id,
        )
