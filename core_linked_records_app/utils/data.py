""" PID utilities related to data objects.
"""
import json
import logging

from core_linked_records_app.utils import exceptions
from core_linked_records_app.utils import (
    xml as pid_xml_utils,
    json as pid_json_utils,
    dict as pid_dict_utils,
)
from core_main_app.components.template.models import Template
from core_main_app.utils.json_utils import load_json_string
from xml_utils.commons.exceptions import XPathError
from xml_utils.xpath import create_tree_from_xpath
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


def set_pid_value_for_data(data, pid_path, pid_value):
    """Set the document PID into XML data and update `content` in place.

    Args:
        data:
        pid_path:
        pid_value:
    """
    if data.template.format == Template.XSD:
        pid_xpath = pid_xml_utils.get_xpath_with_target_namespace(
            pid_xml_utils.get_xpath_from_dot_notation(pid_path),
            data.template.content,
        )

        target_namespace = pid_xml_utils.get_target_namespace_for_xsd_string(
            data.template.content
        )
        xml_tree = XSDTree.build_tree(data.content)

        xml_tree = create_tree_from_xpath(
            pid_xpath, xml_tree, target_namespace
        )
        pid_xml_utils.set_value_at_xpath(
            xml_tree, pid_xpath, pid_value, target_namespace
        )
        data.content = XSDTree.tostring(xml_tree)
    elif data.template.format == Template.JSON:
        json_content = load_json_string(data.content)
        json_content = pid_json_utils.set_value_at_dict_path(
            json_content, pid_path, pid_value
        )
        data.content = json.dumps(json_content)
    else:
        error_message = "Cannot create PID. Invalid template format."
        logger.error(error_message)
        raise exceptions.PidCreateError(error_message)

    # Update the whole document with the updated XML content
    data.convert_to_file()
    data.convert_to_dict()


def get_pid_value_for_data(data, pid_path):
    """Retrieve value located at `pid_path` of the data passed in parameter.

    Args:
        data:
        pid_path:

    Returns:
        str - Persitstent identifier
    """
    if data.template.format == Template.XSD:
        # Transform the dot notation path into an XML XPath.
        pid_path = pid_xml_utils.get_xpath_with_target_namespace(
            pid_xml_utils.get_xpath_from_dot_notation(pid_path),
            data.template.content,
        )

        target_namespace = pid_xml_utils.get_target_namespace_for_xsd_string(
            data.template.content
        )
        xml_tree = XSDTree.build_tree(data.content)

        try:  # Get the PID from the `pid_path` value
            pid_value = pid_xml_utils.get_value_at_xpath(
                xml_tree, pid_path, target_namespace
            )
        except XPathError as xpath_error_exc:  # PID path not found in document
            if not pid_xml_utils.can_create_value_at_xpath(
                data.content,
                data.template.content,
                pid_path,
                "http://sample_pid.org",
            ):
                raise exceptions.PidCreateError(
                    f"Cannot create pid value at {pid_path}"
                ) from xpath_error_exc
            pid_value = None
    elif data.template.format == Template.JSON:
        json_content = load_json_string(data.content)
        pid_value = pid_dict_utils.get_value_from_dot_notation(
            json_content, pid_path
        )

        # PID path has not been found in document and cannot be created.
        if (
            pid_value is None
            and not pid_json_utils.can_create_value_at_dict_path(
                json_content,
                data.template.content,
                pid_path,
                "http://sample_pid.org",
            )
        ):
            raise exceptions.PidCreateError(
                f"Cannot create pid value at {pid_path}"
            )
    else:
        error_message = "Cannot create PID. Invalid template format."
        logger.error(error_message)
        raise exceptions.InvalidPidError(error_message)

    # Return the PID and clean it up if it ends with a '/'.
    return (
        pid_value[:-1]
        if isinstance(pid_value, str) and pid_value.endswith("/")
        else pid_value
    )
