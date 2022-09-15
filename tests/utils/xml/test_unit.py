""" Unit tests for core_linked_records_app.utils.xml
"""
from unittest import TestCase


class TestGetXpathFromDotNotation(TestCase):
    """Test Get Xpath From Dot Notation"""

    def test_attributes_are_not_prepended_for_namespaces(self):
        """test_attributes_are_not_prepended_for_namespaces"""

        pass

    def test_dot_notation_transformed_correctly(self):
        """test_dot_notation_transformed_correctly"""

        pass


class TestGetXpathWithTargetNamespace(TestCase):
    """TestGetXpathWithTargetNamespace"""

    pass


class TestSetValueAtXpath(TestCase):
    """Test Set Value At Xpath"""

    def test_invalid_xpath_raises_error(self):
        """test_invalid_xpath_raises_error"""

        pass

    def test_element_xpath_replaced(self):
        """test_element_xpath_replaced"""

        pass

    def test_attribute_xpath_replaced(self):
        """test_attribute_xpath_replaced"""

        pass


class TestGetValueAtXpath(TestCase):
    """Test Get Value At Xpath"""

    def test_not_existing_xpath_raises_error(self):
        """test_not_existing_xpath_raises_error"""

        pass

    def test_invalid_xpath_raises_error(self):
        """test_invalid_xpath_raises_error"""

        pass

    def test_attribute_xpath_returns_value(self):
        """test_attribute_xpath_returns_value"""

        pass

    def test_element_xpath_returns_value(self):
        """test_element_xpath_returns_value"""

        pass
