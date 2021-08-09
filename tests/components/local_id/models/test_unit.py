""" Unit tests for core_linked_records_app.components.local_id.models
"""
from unittest import TestCase

from mongoengine import errors as mongoengine_errors
from unittest.mock import patch

from core_linked_records_app.components.local_id.models import LocalId
from core_main_app.commons import exceptions


class TestGetByName(TestCase):
    @patch.object(LocalId, "objects")
    def test_local_id_get_does_not_exist_raises_does_not_exist_error(
        self, mock_objects
    ):
        mock_objects.get.side_effect = mongoengine_errors.DoesNotExist(
            "mock_objects_get_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            LocalId.get_by_name("mock_record_name")

    @patch.object(LocalId, "objects")
    def test_local_id_get_failure_raises_model_error(self, mock_objects):
        mock_objects.get.side_effect = Exception("mock_objects_get_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.get_by_name("mock_record_name")

    @patch.object(LocalId, "objects")
    def test_returns_local_id_get_output(self, mock_objects):
        expected_result = "mock_get_by_name"
        mock_objects.get.return_value = expected_result

        self.assertEquals(LocalId.get_by_name("mock_record_name"), expected_result)


class TestGetByClassAndId(TestCase):
    @patch.object(LocalId, "objects")
    def test_local_id_get_does_not_exist_raises_does_not_exist_error(
        self, mock_objects
    ):
        mock_objects.get.side_effect = mongoengine_errors.DoesNotExist(
            "mock_objects_get_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id")

    @patch.object(LocalId, "objects")
    def test_local_id_get_failure_raises_model_error(self, mock_objects):
        mock_objects.get.side_effect = Exception("mock_objects_get_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id")

    @patch.object(LocalId, "objects")
    def test_returns_local_id_get_output(self, mock_objects):
        expected_result = "mock_get_by_name"
        mock_objects.get.return_value = expected_result

        self.assertEquals(
            LocalId.get_by_class_and_id("mock_record_class", "mock_record_id"),
            expected_result,
        )


class TestUpdate(TestCase):
    def setUp(self):
        self.mock_local_id = LocalId()

    @patch.object(LocalId, "save")
    def test_local_id_save_not_unique_error_raises_not_unique_error(self, mock_save):
        mock_save.side_effect = mongoengine_errors.NotUniqueError(
            "mock_save_not_unique_error"
        )

        with self.assertRaises(exceptions.NotUniqueError):
            LocalId.upsert(self.mock_local_id)

    @patch.object(LocalId, "save")
    def test_local_id_save_failure_raises_model_error(self, mock_save):
        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(exceptions.ModelError):
            LocalId.upsert(self.mock_local_id)

    @patch.object(LocalId, "save")
    def test_returns_local_id_get_output(self, mock_save):
        expected_result = "mock_get_by_name"
        mock_save.return_value = expected_result

        self.assertEquals(
            LocalId.upsert(self.mock_local_id),
            expected_result,
        )
