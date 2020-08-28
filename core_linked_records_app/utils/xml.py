""" XML utilities functions
"""
from xml_utils.xsd_tree.operations.namespaces import (
    get_target_namespace,
    get_namespaces,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree


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


def get_xpath_with_target_namespace(xpath, xsd_string):
    """Adds target namespace to a given XPath

    Params:
        xpath:
        xsd_string:

    Returns:

    """
    namespaces = get_target_namespace(
        XSDTree.build_tree(xsd_string), get_namespaces(xsd_string)
    )

    xpath = xpath.format(namespaces[1])

    if namespaces[1] == "":
        xpath = xpath.replace(":", "")
        namespaces = None
    else:
        namespaces = {namespaces[1]: namespaces[0]}

    return xpath, namespaces


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

    return xpath_value
