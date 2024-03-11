""" Unit tests for `core_linked_records_app.utils.data`.
"""
from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.components.template.models import Template
from xml_utils.commons import exceptions as xml_utils_exceptions
from core_linked_records_app.utils import data as data_utils, exceptions


class TestSetPidValueForDataForXMLData(TestCase):
    """Unit tests for `set_pid_value_for_data` function, limiting to XML data."""

    def setUp(self):
        """setUp"""
        template_format = Template.XSD
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {
            "data": self.mock_data,
            "pid_path": "mock_pid_path",
            "pid_value": "pid_value",
        }

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_xpath_with_target_namespace_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_get_xpath_with_target_namespace_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.get_xpath_with_target_namespace.assert_called_with(
            mock_pid_xml_utils.get_xpath_from_dot_notation(
                self.kwargs["pid_path"]
            ),
            self.kwargs["data"].template.content,
        )

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_target_namespace_for_xsd_string_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_get_target_namespace_for_xsd_string_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.get_target_namespace_for_xsd_string.assert_called_with(
            self.kwargs["data"].template.content
        )

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_xsdtree_build_tree_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_xsdtree_build_tree_called"""
        mock_data_init_content = deepcopy(self.mock_data.content)
        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_xsd_tree.build_tree.assert_called_with(mock_data_init_content)

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_create_tree_from_xpath_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_create_tree_from_xpath_called"""
        mock_pid_xpath = MagicMock()
        mock_target_namespace = MagicMock()
        mock_xml_tree = MagicMock()
        mock_pid_xml_utils.get_xpath_with_target_namespace.return_value = (
            mock_pid_xpath
        )
        mock_pid_xml_utils.get_target_namespace_for_xsd_string.return_value = (
            mock_target_namespace
        )
        mock_xsd_tree.build_tree.return_value = mock_xml_tree

        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_create_tree_from_xpath.assert_called_with(
            mock_pid_xpath, mock_xml_tree, mock_target_namespace
        )

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_set_value_at_xpath_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_set_value_at_xpath_called"""
        mock_pid_xpath = MagicMock()
        mock_target_namespace = MagicMock()
        mock_xml_tree = MagicMock()
        mock_pid_xml_utils.get_xpath_with_target_namespace.return_value = (
            mock_pid_xpath
        )
        mock_pid_xml_utils.get_target_namespace_for_xsd_string.return_value = (
            mock_target_namespace
        )
        mock_create_tree_from_xpath.return_value = mock_xml_tree

        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.set_value_at_xpath.assert_called_with(
            mock_xml_tree,
            mock_pid_xpath,
            self.kwargs["pid_value"],
            mock_target_namespace,
        )

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_xsdtree_to_string_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_xsdtree_to_string_called"""
        mock_xml_tree = MagicMock()
        mock_create_tree_from_xpath.return_value = mock_xml_tree

        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_xsd_tree.tostring.assert_called_with(mock_xml_tree)

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_convert_to_file_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_convert_to_file_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        self.kwargs["data"].convert_to_file.assert_called()

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_convert_to_dict_called(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_convert_to_dict_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        self.kwargs["data"].convert_to_dict.assert_called()

    @patch.object(data_utils, "create_tree_from_xpath")
    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_succesful_execution_returns_none(
        self, mock_pid_xml_utils, mock_xsd_tree, mock_create_tree_from_xpath
    ):
        """test_succesful_execution_returns_none"""
        self.assertIsNone(data_utils.set_pid_value_for_data(**self.kwargs))


class TestSetPidValueForDataForJsonData(TestCase):
    """Unit tests for `set_pid_value_for_data` function, limiting to JSON data."""

    def setUp(self):
        """setUp"""
        template_format = Template.JSON
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {
            "data": self.mock_data,
            "pid_path": "mock_pid_path",
            "pid_value": "pid_value",
        }

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_json_loads_called(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_json_loads_called"""
        mock_data_init_content = deepcopy(self.mock_data.content)
        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_load_json_string.assert_called_with(mock_data_init_content)

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_set_value_at_dict_path_called(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_set_value_at_dict_path_called"""
        mock_json_content = MagicMock()
        mock_load_json_string.return_value = mock_json_content

        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_pid_json_utils.set_value_at_dict_path.assert_called_with(
            mock_json_content,
            self.kwargs["pid_path"],
            self.kwargs["pid_value"],
        )

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_json_dumps_called(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_json_dumps_called"""
        mock_json_content = MagicMock()
        mock_pid_json_utils.set_value_at_dict_path.return_value = (
            mock_json_content
        )

        data_utils.set_pid_value_for_data(**self.kwargs)

        mock_json.dumps.assert_called_with(mock_json_content)

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_convert_to_file_called(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_convert_to_file_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        self.kwargs["data"].convert_to_file.assert_called()

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_convert_to_dict_called(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_convert_to_dict_called"""
        data_utils.set_pid_value_for_data(**self.kwargs)

        self.kwargs["data"].convert_to_dict.assert_called()

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "load_json_string")
    @patch.object(data_utils, "json")
    def test_succesful_execution_returns_none(
        self, mock_json, mock_load_json_string, mock_pid_json_utils
    ):
        """test_succesful_execution_returns_none"""
        self.assertIsNone(data_utils.set_pid_value_for_data(**self.kwargs))


class TestSetPidValueForDataForUnsupportedFormats(TestCase):
    """Unit tests for `set_pid_value_for_data` function, limiting to unsupported
    formats."""

    def setUp(self):
        """setUp"""
        template_format = "mock_unsupported_format"
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {
            "data": self.mock_data,
            "pid_path": "mock_pid_path",
            "pid_value": "pid_value",
        }

    @patch.object(data_utils, "logger")
    def test_logger_error_called(self, mock_logger):
        """test_logger_error_called"""
        with self.assertRaises(exceptions.PidCreateError):
            data_utils.set_pid_value_for_data(**self.kwargs)

        mock_logger.error.assert_called()


class TestGetPidValueForDataForXMLData(TestCase):
    """Unit tests for `get_pid_value_for_data` function, limiting to XML data."""

    def setUp(self):
        """setUp"""
        template_format = Template.XSD
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {"data": self.mock_data, "pid_path": "mock_pid_path"}

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_xpath_with_target_namespace_called(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_get_xpath_with_target_namespace_called"""
        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.get_xpath_with_target_namespace.assert_called_with(
            mock_pid_xml_utils.get_xpath_from_dot_notation(
                self.kwargs["pid_path"]
            ),
            self.kwargs["data"].template.content,
        )

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_target_namespace_for_xsd_string_called(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_get_target_namespace_for_xsd_string_called"""
        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.get_target_namespace_for_xsd_string.assert_called_with(
            self.kwargs["data"].template.content
        )

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_xsd_tree_build_tree_called(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_xsd_tree_build_tree_called"""
        mock_data_init_content = self.kwargs["data"].content
        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_xsd_tree.build_tree.assert_called_with(mock_data_init_content)

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_value_at_xpath_called(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_get_value_at_xpath_called"""
        mock_xml_tree = MagicMock()
        mock_pid_xpath = MagicMock()
        mock_target_namespace = MagicMock()

        mock_pid_xml_utils.get_xpath_with_target_namespace.return_value = (
            mock_pid_xpath
        )
        mock_pid_xml_utils.get_target_namespace_for_xsd_string.return_value = (
            mock_target_namespace
        )
        mock_xsd_tree.build_tree.return_value = mock_xml_tree

        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.get_value_at_xpath.assert_called_with(
            mock_xml_tree, mock_pid_xpath, mock_target_namespace
        )

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_value_at_xpath_error_call_can_create_value_at_xpath(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_get_value_at_xpath_error_call_can_create_value_at_xpath"""
        mock_data_init_content = self.kwargs["data"].content
        mock_pid_xpath = MagicMock()

        mock_pid_xml_utils.get_xpath_with_target_namespace.return_value = (
            mock_pid_xpath
        )
        mock_pid_xml_utils.get_value_at_xpath.side_effect = (
            xml_utils_exceptions.XPathError(
                "mock_get_value_at_xpath_exception"
            )
        )

        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_xml_utils.can_create_value_at_xpath.assert_called_with(
            mock_data_init_content,
            self.kwargs["data"].template.content,
            mock_pid_xpath,
            "http://sample_pid.org",
        )

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_can_create_value_at_xpath_false_raises_pid_create_error(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_can_create_value_at_xpath_false_raises_pid_create_error"""
        mock_pid_xml_utils.get_value_at_xpath.side_effect = (
            xml_utils_exceptions.XPathError(
                "mock_get_value_at_xpath_exception"
            )
        )
        mock_pid_xml_utils.can_create_value_at_xpath.return_value = False

        with self.assertRaises(exceptions.PidCreateError):
            data_utils.get_pid_value_for_data(**self.kwargs)

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_get_value_at_xpath_error_returns_none(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_get_value_at_xpath_error_returns_none"""
        mock_pid_xml_utils.get_value_at_xpath.side_effect = (
            xml_utils_exceptions.XPathError(
                "mock_get_value_at_xpath_exception"
            )
        )
        mock_pid_xml_utils.can_create_value_at_xpath.return_value = True

        self.assertIsNone(data_utils.get_pid_value_for_data(**self.kwargs))

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_successful_executiopn_returns_pid_value(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_successful_executiopn_returns_pid_value"""
        mock_pid_value = "mock_pid_value"

        mock_pid_xml_utils.get_value_at_xpath.return_value = mock_pid_value

        self.assertEqual(
            data_utils.get_pid_value_for_data(**self.kwargs), mock_pid_value
        )

    @patch.object(data_utils, "XSDTree")
    @patch.object(data_utils, "pid_xml_utils")
    def test_pid_value_truncated_if_ending_with_slash(
        self, mock_pid_xml_utils, mock_xsd_tree
    ):
        """test_pid_value_truncated_if_ending_with_slash"""
        mock_pid_value = "mock_pid_value/"

        mock_pid_xml_utils.get_value_at_xpath.return_value = mock_pid_value

        self.assertEqual(
            data_utils.get_pid_value_for_data(**self.kwargs),
            mock_pid_value[:-1],
        )


class TestGetPidValueForDataForJsonData(TestCase):
    """Unit tests for `get_pid_value_for_data` function, limiting to JSON data."""

    def setUp(self):
        """setUp"""
        template_format = Template.JSON
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {
            "data": self.mock_data,
            "pid_path": "mock_pid_path",
        }

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_json_loads_called(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_json_loads_called"""
        mock_data_init_content = self.kwargs["data"].content
        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_load_json_string.assert_called_with(mock_data_init_content)

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_get_value_from_dot_notation_called(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_get_value_from_dot_notation_called"""
        mock_json_content = MagicMock()
        mock_load_json_string.return_value = mock_json_content

        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_dict_utils.get_value_from_dot_notation.assert_called_with(
            mock_json_content, self.kwargs["pid_path"]
        )

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_can_create_value_at_dict_path_called(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_cannot_create_value_at_dict_path_raises_pid_create_error"""
        mock_json_content = MagicMock()

        mock_pid_dict_utils.get_value_from_dot_notation.return_value = None
        mock_load_json_string.return_value = mock_json_content

        data_utils.get_pid_value_for_data(**self.kwargs)

        mock_pid_json_utils.can_create_value_at_dict_path.assert_called_with(
            mock_json_content,
            self.kwargs["data"].template.content,
            self.kwargs["pid_path"],
            "http://sample_pid.org",
        )

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_cannot_create_value_at_dict_path_raises_pid_create_error(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_cannot_create_value_at_dict_path_raises_pid_create_error"""
        mock_pid_dict_utils.get_value_from_dot_notation.return_value = None
        mock_pid_json_utils.can_create_value_at_dict_path.return_value = False

        with self.assertRaises(exceptions.PidCreateError):
            data_utils.get_pid_value_for_data(**self.kwargs)

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_successful_execution_returns_pid_value(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_successful_execution_returns_pid_value"""
        mock_pid_value = "mock_pid_value"

        mock_pid_dict_utils.get_value_from_dot_notation.return_value = (
            mock_pid_value
        )

        self.assertEqual(
            data_utils.get_pid_value_for_data(**self.kwargs), mock_pid_value
        )

    @patch.object(data_utils, "pid_json_utils")
    @patch.object(data_utils, "pid_dict_utils")
    @patch.object(data_utils, "load_json_string")
    def test_pid_value_truncated_if_ending_with_slash(
        self, mock_load_json_string, mock_pid_dict_utils, mock_pid_json_utils
    ):
        """test_pid_value_truncated_if_ending_with_slash"""
        mock_pid_value = "mock_pid_value/"

        mock_pid_dict_utils.get_value_from_dot_notation.return_value = (
            mock_pid_value
        )

        self.assertEqual(
            data_utils.get_pid_value_for_data(**self.kwargs),
            mock_pid_value[:-1],
        )


class TestGetPidValueForDataForUnsupportedFormats(TestCase):
    """Unit tests for `get_pid_value_for_data` function, limiting to unsupported
    formats."""

    def setUp(self):
        """setUp"""
        template_format = "mock_unsupported_format"
        self.mock_data = MagicMock()
        self.mock_data.template.format = template_format

        self.kwargs = {
            "data": self.mock_data,
            "pid_path": "pid_path",
        }

    @patch.object(data_utils, "logger")
    def test_logger_error_called(self, mock_logger):
        """test_logger_error_called"""
        with self.assertRaises(exceptions.InvalidPidError):
            data_utils.get_pid_value_for_data(**self.kwargs)

        mock_logger.error.assert_called()
