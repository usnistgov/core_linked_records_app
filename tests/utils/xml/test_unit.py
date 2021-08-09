""" Unit tests for core_linked_records_app.utils.xml
"""
from unittest import TestCase


class TestGetXpathFromDotNotation(TestCase):
    def test_attributes_are_not_prepended_for_namespaces(self):
        pass

    def test_dot_notation_transformed_correctly(self):
        pass


class TestGetXpathWithTargetNamespace(TestCase):
    pass


class TestSetValueAtXpath(TestCase):
    def test_invalid_xpath_raises_error(self):
        pass

    def test_element_xpath_replaced(self):
        pass

    def test_attribute_xpath_replaced(self):
        pass


class TestGetValueAtXpath(TestCase):
    def test_not_existing_xpath_raises_error(self):
        pass

    def test_invalid_xpath_raises_error(self):
        pass

    def test_attribute_xpath_returns_value(self):
        pass

    def test_element_xpath_returns_value(self):
        pass
