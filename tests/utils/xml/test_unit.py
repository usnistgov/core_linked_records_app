""" Unit tests for `core_linked_records_app.utils.xml`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from core_linked_records_app.utils import xml as linked_records_xml_utils
from xml_utils.commons import exceptions as xml_utils_exceptions


class TestGetValueAtXPath(TestCase):
    """Unit tests for `get_value_at_xpath` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "xml_tree": MagicMock(),
            "xpath": MagicMock(),
            "namespaces": MagicMock(),
        }

    def test_xml_tree_xpath_called(self):
        """test_xml_tree_xpath_called"""
        with self.assertRaises(xml_utils_exceptions.XPathError):
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs)

        self.mock_kwargs["xml_tree"].xpath.assert_called_with(
            self.mock_kwargs["xpath"],
            namespaces=self.mock_kwargs["namespaces"],
        )

    def test_more_than_one_xpath_found_raises_xpath_error(self):
        """test_more_than_one_xpath_found_raises_xpath_error"""
        self.mock_kwargs["xml_tree"].xpath.return_value = [MagicMock()] * 2

        with self.assertRaises(xml_utils_exceptions.XPathError):
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs)

    def test_no_xpath_found_raises_xpath_error(self):
        """test_no_xpath_found_raises_xpath_error"""
        self.mock_kwargs["xml_tree"].xpath.return_value = []

        with self.assertRaises(xml_utils_exceptions.XPathError):
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs)

    def test_retrieve_xpath_element_text(self):
        """test_retrieve_xpath_element_text"""
        mock_xpath_element = MagicMock()
        self.mock_kwargs["xml_tree"].xpath.return_value = [mock_xpath_element]

        self.assertEqual(
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs),
            str(mock_xpath_element.text),
        )

    def test_retrieve_xpath_element_if_text_raises_attribute_error(self):
        """test_retrieve_xpath_element_if_text_raises_attribute_error"""
        mock_xpath_element = "mock_xpath"
        self.mock_kwargs["xml_tree"].xpath.return_value = [mock_xpath_element]

        self.assertEqual(
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs),
            str(mock_xpath_element),
        )

    def test_retrieve_xpath_element_none_returns_none(self):
        """test_retrieve_xpath_element_none_returns_none"""
        mock_xpath_element = None
        self.mock_kwargs["xml_tree"].xpath.return_value = [mock_xpath_element]

        self.assertIsNone(
            linked_records_xml_utils.get_value_at_xpath(**self.mock_kwargs)
        )


class TestCanCreateValueAtXpath(TestCase):
    """Unit tests for `can_create_value_at_xpath` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "xml_string": MagicMock(),
            "xsd_string": MagicMock(),
            "xpath": MagicMock(),
            "value": MagicMock(),
        }

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_get_target_namespace_for_xsd_string_called(
        self,
        mock_get_target_namespace_for_xsd_string,
        mock_xsd_tree,  # noqa, pylint: disable=unused-argument
        mock_create_tree_from_xpath,  # noqa, pylint: disable=unused-argument
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,  # noqa, pylint: disable=unused-argument
    ):
        """test_get_target_namespace_for_xsd_string_called"""
        linked_records_xml_utils.can_create_value_at_xpath(**self.mock_kwargs)

        mock_get_target_namespace_for_xsd_string.assert_called_with(
            self.mock_kwargs["xsd_string"]
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_xsd_tree_build_tree_called(
        self,
        mock_get_target_namespace_for_xsd_string,  # noqa, pylint: disable=unused-argument
        mock_xsd_tree,
        mock_create_tree_from_xpath,  # noqa, pylint: disable=unused-argument
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,  # noqa, pylint: disable=unused-argument
    ):
        """test_xsd_tree_build_tree_called"""
        linked_records_xml_utils.can_create_value_at_xpath(**self.mock_kwargs)

        mock_xsd_tree.build_tree.assert_has_calls(
            [
                call(self.mock_kwargs["xml_string"]),
                call(self.mock_kwargs["xsd_string"]),
            ]
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_create_tree_from_xpath_called(
        self,
        mock_get_target_namespace_for_xsd_string,
        mock_xsd_tree,
        mock_create_tree_from_xpath,
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,  # noqa, pylint: disable=unused-argument
    ):
        """test_create_tree_from_xpath_called"""
        mock_target_namespace = MagicMock()
        mock_xml_tree = MagicMock()

        mock_get_target_namespace_for_xsd_string.return_value = (
            mock_target_namespace
        )
        mock_xsd_tree.build_tree.return_value = mock_xml_tree

        linked_records_xml_utils.can_create_value_at_xpath(**self.mock_kwargs)

        mock_create_tree_from_xpath.assert_called_with(
            self.mock_kwargs["xpath"],
            mock_xml_tree,
            mock_target_namespace,
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_set_value_at_xpath_called(
        self,
        mock_get_target_namespace_for_xsd_string,
        mock_xsd_tree,  # noqa, pylint: disable=unused-argument
        mock_create_tree_from_xpath,
        mock_set_value_at_xpath,
        mock_validate_xml_data,  # noqa, pylint: disable=unused-argument
    ):
        """test_set_value_at_xpath_called"""
        mock_target_namespace = MagicMock()
        mock_modified_xml_tree = MagicMock()

        mock_get_target_namespace_for_xsd_string.return_value = (
            mock_target_namespace
        )
        mock_create_tree_from_xpath.return_value = mock_modified_xml_tree

        linked_records_xml_utils.can_create_value_at_xpath(**self.mock_kwargs)

        mock_set_value_at_xpath.assert_called_with(
            mock_modified_xml_tree,
            self.mock_kwargs["xpath"],
            self.mock_kwargs["value"],
            mock_target_namespace,
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_validate_xml_data_called(
        self,
        mock_get_target_namespace_for_xsd_string,  # noqa, pylint: disable=unused-argument
        mock_xsd_tree,
        mock_create_tree_from_xpath,
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,
    ):
        """test_validate_xml_data_called"""
        mock_xsd_built_tree = MagicMock()
        mock_modified_xml_tree = MagicMock()

        mock_xsd_tree.build_tree.return_value = mock_xsd_built_tree
        mock_create_tree_from_xpath.return_value = mock_modified_xml_tree

        linked_records_xml_utils.can_create_value_at_xpath(**self.mock_kwargs)

        mock_validate_xml_data.assert_called_with(
            mock_xsd_built_tree,
            mock_modified_xml_tree,
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_validate_xml_data_not_none_returns_false(
        self,
        mock_get_target_namespace_for_xsd_string,  # noqa, pylint: disable=unused-argument
        mock_xsd_tree,  # noqa, pylint: disable=unused-argument
        mock_create_tree_from_xpath,  # noqa, pylint: disable=unused-argument
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,
    ):
        """test_validate_xml_data_not_none_returns_false"""
        mock_validate_xml_data.return_value = "mock_validate_xml_error"

        self.assertFalse(
            linked_records_xml_utils.can_create_value_at_xpath(
                **self.mock_kwargs
            )
        )

    @patch.object(linked_records_xml_utils, "validate_xml_data")
    @patch.object(linked_records_xml_utils, "set_value_at_xpath")
    @patch.object(linked_records_xml_utils, "create_tree_from_xpath")
    @patch.object(linked_records_xml_utils, "XSDTree")
    @patch.object(
        linked_records_xml_utils, "get_target_namespace_for_xsd_string"
    )
    def test_successful_execution_returns_true(
        self,
        mock_get_target_namespace_for_xsd_string,  # noqa, pylint: disable=unused-argument
        mock_xsd_tree,  # noqa, pylint: disable=unused-argument
        mock_create_tree_from_xpath,  # noqa, pylint: disable=unused-argument
        mock_set_value_at_xpath,  # noqa, pylint: disable=unused-argument
        mock_validate_xml_data,
    ):
        """test_successful_execution_returns_true"""
        mock_validate_xml_data.return_value = None

        self.assertTrue(
            linked_records_xml_utils.can_create_value_at_xpath(
                **self.mock_kwargs
            )
        )
