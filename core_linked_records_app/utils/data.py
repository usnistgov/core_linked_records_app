""" PID utilities related to data objects.
"""

from xml_utils.xpath import create_tree_from_xpath
from xml_utils.xsd_tree.xsd_tree import XSDTree
from core_linked_records_app.utils.xml import (
    get_target_namespace_for_xsd_string,
    set_value_at_xpath,
    get_value_at_xpath,
    can_create_value_at_xpath,
)


def set_pid_value_for_data(data, pid_xpath, pid_value):
    """Set the document PID into XML data and update `xml_content` in place.

    Args:
        data:
        pid_xpath:
        pid_value:
    """
    target_namespace = get_target_namespace_for_xsd_string(data.template.content)
    xml_tree = XSDTree.build_tree(data.xml_content)

    xml_tree = create_tree_from_xpath(pid_xpath, xml_tree, target_namespace)
    set_value_at_xpath(xml_tree, pid_xpath, pid_value, target_namespace)
    data.xml_content = XSDTree.tostring(xml_tree)

    # Update the whole document with the updated XML content
    data.convert_to_file()
    data.convert_to_dict()


def get_pid_value_for_data(data, pid_xpath):
    """Retrieve value located at `pid_xpath` of the data passed in parameter.

    Args:
        data:
        pid_xpath:

    Returns:
        str - Persitstent identifier
    """
    target_namespace = get_target_namespace_for_xsd_string(data.template.content)
    xml_tree = XSDTree.build_tree(data.xml_content)

    try:  # Get the PID from the `pid_xpath` value
        pid_value = get_value_at_xpath(xml_tree, pid_xpath, target_namespace)
        if type(pid_value) == str and pid_value.endswith(
            "/"
        ):  # Cleanup PID if it ends with a '/'
            pid_value = pid_value[:-1]
    except AssertionError:  # PID XPath not found in document
        assert can_create_value_at_xpath(
            data.xml_content, data.template.content, pid_xpath, "http://sample_pid.org"
        )
        pid_value = None

    return pid_value
