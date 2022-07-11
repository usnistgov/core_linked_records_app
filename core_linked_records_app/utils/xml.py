""" XML utilities functions
"""
import logging

from core_main_app.utils.xml import validate_xml_data
from xml_utils.xpath import create_tree_from_xpath
from xml_utils.xsd_tree.operations.namespaces import (
    get_target_namespace,
    get_namespaces,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


def get_xpath_from_dot_notation(dot_notation_path):
    """Transform MongoDB dot notation to XPath

    Params:
        dot_notation_path:

    Returns:

    """
    dot_notation_elements = [
        "{0}:%s" % path if not path.startswith("@") else path
        for path in dot_notation_path.split(".")
    ]

    xpath = "/%s" % "/".join(dot_notation_elements)
    return xpath


def get_target_namespace_for_xsd_string(xsd_string):
    """Retrieve target namespace given a XSD string.

    Args:
        xsd_string:

    Returns:
        dict|None - a dictionary containing namespace name as key, and url as
            value. If no target namespace have been defiend, None is returned.
    """
    xml_tree = XSDTree.build_tree(xsd_string)
    target_namespace, target_namespace_prefix = get_target_namespace(
        xml_tree, get_namespaces(xsd_string)
    )

    if target_namespace_prefix == "":  # No target namespace have been defined
        namespace = None
    else:  # Target namespace is defined
        namespace = {target_namespace_prefix: target_namespace}

    return namespace


def get_xpath_with_target_namespace(xpath, xsd_string):
    """Adds target namespace to a given XPath

    Params:
        xpath:
        xsd_string:

    Returns:

    """
    target_namespace = get_target_namespace_for_xsd_string(xsd_string)

    xpath = xpath.format(
        list(target_namespace.keys())[0] if target_namespace is not None else ""
    )

    if target_namespace is None:
        xpath = xpath.replace(":", "")

    return xpath


def set_value_at_xpath(xml_tree, xpath, value, namespaces):
    """Set value for a given XPath

    Params:
        xml_tree:
        xpath:
        value:
        namespaces:

    Returns:

    """
    try:
        xml_tree.xpath(xpath, namespaces=namespaces)[0].text = value
    except AttributeError:
        xpath_list = xpath.split("/")
        attribute = xpath_list[-1].replace("@", "")
        xpath = "/%s" % "/".join(xpath_list[:-1])

        xml_tree.xpath(xpath, namespaces=namespaces)[0].attrib[attribute] = value


def get_value_at_xpath(xml_tree, xpath, namespaces):
    """Retrieve value in XML given a XPath

    Params:
        xml_tree:
        xpath:
        namespaces:

    Returns:

    """
    xpath_element_list = xml_tree.xpath(xpath, namespaces=namespaces)

    # Assert that we found exactly one element matching the given xpath
    assert len(xpath_element_list) == 1

    try:
        xpath_value = xpath_element_list[0].text
    except AttributeError:  # XPath points to an attribute
        xpath_value = xpath_element_list[0]

    return str(xpath_value) if xpath_value else xpath_value


def can_create_value_at_xpath(xml_string, xsd_string, xpath, value):
    """Evaluate if a value can be set in an XML file at a given XPath

    Params:
        xml_string:
        xsd_string:
        xpath:
        value:

    Returns:
        bool - True if the value can be created, False otherwise.
    """
    try:
        # Replace the current by the modified tree (containing mock PID) and
        # force document PID to be regenerated.
        target_namespace = get_target_namespace_for_xsd_string(xsd_string)
        xml_tree = XSDTree.build_tree(xml_string)

        modified_xml_tree = create_tree_from_xpath(xpath, xml_tree, target_namespace)
        set_value_at_xpath(modified_xml_tree, xpath, value, target_namespace)
        xsd_tree = XSDTree.build_tree(xsd_string)
        assert validate_xml_data(xsd_tree, modified_xml_tree) is None
        return True
    except Exception as exc:
        logger.info(f"Function 'can_create_url_at_xpath' raised {str(exc)}")
        return False
