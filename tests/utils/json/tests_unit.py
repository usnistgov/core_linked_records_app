""" Unit tests for `core_linked_records.utils.json` package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.utils import json as json_utils


class TestSetValueAtDictPath(TestCase):
    """Unit tests for `set_value_at_dict_path` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "dictionary": MagicMock(),
            "dot_notation": MagicMock(),
            "value": MagicMock(),
        }

    def test_no_key_raises_key_error(self):
        """test_no_key_raises_key_error"""
        self.mock_kwargs["dot_notation"] = None  # noqa

        with self.assertRaises(KeyError):
            json_utils.set_value_at_dict_path(**self.mock_kwargs)

    def test_single_key_returns_modified_dictionary(self):
        """test_single_key_returns_modified_dictionary"""
        self.mock_kwargs["dictionary"] = {"key1": MagicMock()}  # noqa
        self.mock_kwargs["dot_notation"] = "key1"  # noqa

        self.assertEqual(
            json_utils.set_value_at_dict_path(**self.mock_kwargs),
            {"key1": self.mock_kwargs["value"]},
        )

    def test_multiple_key_returns_modified_dictionary(self):
        """test_multiple_key_returns_modified_dictionary"""
        self.mock_kwargs["dictionary"] = {  # noqa
            "key1": {"key2": MagicMock()}
        }
        self.mock_kwargs["dot_notation"] = "key1.key2"  # noqa

        self.assertEqual(
            json_utils.set_value_at_dict_path(**self.mock_kwargs),
            {"key1": {"key2": self.mock_kwargs["value"]}},
        )


class TestCanCreateValueAtDictPath(TestCase):
    """Unit tests for `can_create_value_at_dict_path` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "json_dict": MagicMock(),
            "template_dict": MagicMock(),
            "dict_path": MagicMock(),
            "value": MagicMock(),
        }

    @patch.object(json_utils, "validate_json_data")
    @patch.object(json_utils, "set_value_at_dict_path")
    def test_set_value_at_dict_path_called(
        self,
        mock_set_value_at_dict_path,
        mock_validate_json_data,  # noqa, pylint: disable=unused-argument
    ):
        """test_set_value_at_dict_path_called"""
        json_utils.can_create_value_at_dict_path(**self.mock_kwargs)

        mock_set_value_at_dict_path.assert_called_with(
            self.mock_kwargs["json_dict"],
            self.mock_kwargs["dict_path"],
            self.mock_kwargs["value"],
        )

    @patch.object(json_utils, "validate_json_data")
    @patch.object(json_utils, "set_value_at_dict_path")
    def test_validate_json_data_called(
        self,
        mock_set_value_at_dict_path,  # noqa, pylint: disable=unused-argument
        mock_validate_json_data,
    ):
        """test_validate_json_data_called"""
        json_utils.can_create_value_at_dict_path(**self.mock_kwargs)

        mock_validate_json_data.assert_called_with(
            self.mock_kwargs["json_dict"], self.mock_kwargs["template_dict"]
        )

    @patch.object(json_utils, "validate_json_data")
    @patch.object(json_utils, "set_value_at_dict_path")
    def test_validate_json_data_not_none_returns_false(
        self,
        mock_set_value_at_dict_path,  # noqa, pylint: disable=unused-argument
        mock_validate_json_data,
    ):
        """test_validate_json_data_not_none_returns_false"""
        mock_validate_json_data.return_value = "mock_validation_error"
        self.assertFalse(
            json_utils.can_create_value_at_dict_path(**self.mock_kwargs)
        )

    @patch.object(json_utils, "validate_json_data")
    @patch.object(json_utils, "set_value_at_dict_path")
    def test_successful_execution_returns_true(
        self,
        mock_set_value_at_dict_path,  # noqa, pylint: disable=unused-argument
        mock_validate_json_data,
    ):
        """test_successful_execution_returns_true"""
        mock_validate_json_data.return_value = None
        self.assertTrue(
            json_utils.can_create_value_at_dict_path(**self.mock_kwargs)
        )
