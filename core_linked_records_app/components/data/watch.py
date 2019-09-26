""" Signals to trigger before Data save
"""
import json
import logging

from django.urls import reverse
from rest_framework import status

from core_linked_records_app.settings import PID_XPATH, HANDLE_SYSTEMS, SERVER_URI
from core_linked_records_app.utils.xml import get_xpath_from_dot_notation, \
    get_xpath_with_target_namespace, get_value_at_xpath, set_value_at_xpath
from core_main_app.components.data.models import Data
from core_main_app.utils.requests_utils.requests_utils import send_get_request, send_put_request
from signals_utils.signals.mongo import signals, connector
from xml_utils.xsd_tree.xsd_tree import XSDTree

LOGGER = logging.getLogger(
    "core_linked_records_app.utils.handle_systems.handle_net"
)


def init():
    """ Connect to Data object events.
    """
    connector.connect(set_data_pid, signals.pre_save, Data)


def set_data_pid(sender, document, **kwargs):
    """ Set the PID in the XML field specified in the settings. If the PID
    already exists and is valid, it is not reset.

    Params:
        sender:
        document:
        kwargs:

    Returns:
    """
    # FIXME remove hard-coded variables
    default_system = list(HANDLE_SYSTEMS.keys())[0]
    prefix = "cdcs"

    pid_xpath = get_xpath_from_dot_notation(PID_XPATH)

    # Retrieve namespaces
    xml_tree = XSDTree.build_tree(document.xml_content)
    pid_xpath, namespaces = get_xpath_with_target_namespace(
        pid_xpath, document.template.content
    )

    # Retrieve element value
    try:
        document_pid = get_value_at_xpath(xml_tree, pid_xpath, namespaces)
    except AssertionError:  # PID XPath not found in document
        return

    # Decide if the PID needs to be generated
    generate_pid = True
    if document_pid is not None and document_pid != "":
        try:
            generate_pid = (
                send_get_request(document_pid).status_code != status.HTTP_200_OK
            )
        except Exception as e:
            LOGGER.info("Exception when fetching local id %s: %s" % (
                document_pid, str(e))
            )

    if generate_pid:  # If the PID needs to be generated
        document_pid_response = send_put_request(
            "%s%s" % (
                SERVER_URI,
                reverse(
                    "core_linked_records_app_rest_handle_record_view",
                    kwargs={
                        "system": default_system,
                        "handle": prefix
                    }
                )
            )
        )

        # FIXME change to remote URL
        document_pid = "%s%s" % (
            SERVER_URI,
            reverse(
                "core_linked_records_app_rest_handle_record_view",
                kwargs={
                    "system": default_system,
                    "handle": json.loads(document_pid_response.content)["handle"]
                }
            )
        )

    # Set the document PID into XML data and update `xml_content`
    set_value_at_xpath(xml_tree, pid_xpath, document_pid, namespaces)
    document.xml_content = XSDTree.tostring(xml_tree)

    # Update the whole document with the updated XML content
    document.convert_to_file()
    document.convert_to_dict()

