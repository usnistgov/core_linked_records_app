""" Unit tests for core_linked_records_app.utils.dict
"""
from unittest import TestCase

from core_linked_records_app.utils.dict import (
    get_value_from_dot_notation,
    is_dot_notation_in_dictionary,
)


class TestGetValueFromDotNotation(TestCase):
    """Tests for get_value_from_dot_notation function"""

    @classmethod
    def setUpClass(cls) -> None:
        """Create test case global variables"""
        cls.mock_dictionary = {
            "root": {"elem11": {"elem21": "value2"}, "elem12": "value1"}
        }

    def test_empty_path_returns_dictionary(self):
        """Test empty path returns dictionary"""
        self.assertDictEqual(
            get_value_from_dot_notation(self.mock_dictionary, ""), self.mock_dictionary
        )

    def test_non_existing_path_returns_none(self):
        """Test non existing path returns None"""
        self.assertIsNone(
            get_value_from_dot_notation(self.mock_dictionary, "root.elem13")
        )

    def test_existing_root_returns_dict_content(self):
        """Test existing root returns dict_content"""
        self.assertDictEqual(
            get_value_from_dot_notation(self.mock_dictionary, "root"),
            self.mock_dictionary["root"],
        )

    def test_existing_deep_key_returns_dict_content(self):
        """Test existing deep key returns dict_content"""
        self.assertEqual(
            get_value_from_dot_notation(self.mock_dictionary, "root.elem11.elem21"),
            self.mock_dictionary["root"]["elem11"]["elem21"],
        )


class TestIsDotNotationInDictionary(TestCase):
    """Tests for is_dot_notation_in_dictionary function"""

    @classmethod
    def setUpClass(cls) -> None:
        """Create test case global variables"""
        cls.mock_dictionary = {
            "root": {"elem11": {"elem21": "value2"}, "elem12": "value1"}
        }

    def test_empty_path_returns_true(self):
        """Test empty path returns True"""
        self.assertTrue(is_dot_notation_in_dictionary(self.mock_dictionary, []))

    def test_non_existing_path_returns_false(self):
        """Test non existing path returns False"""
        self.assertFalse(
            is_dot_notation_in_dictionary(self.mock_dictionary, "root.elem13")
        )

    def test_existing_root_key_returns_true(self):
        """Test existing root key returns True"""
        self.assertTrue(is_dot_notation_in_dictionary(self.mock_dictionary, "root"))

    def test_existing_deep_key_returns_true(self):
        """Test existing deep key returns True"""
        self.assertTrue(
            is_dot_notation_in_dictionary(self.mock_dictionary, "root.elem11.elem21")
        )
