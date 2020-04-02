""" Signals to trigger before Data save
"""
import logging
import re

from django.urls import reverse

from core_linked_records_app.settings import ID_PROVIDER_SYSTEMS, PID_XPATH, SERVER_URI, \
    ID_PROVIDER_PREFIX, PID_FORMAT
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils.xml import get_xpath_from_dot_notation, \
    get_xpath_with_target_namespace, get_value_at_xpath, set_value_at_xpath
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.utils.requests_utils.requests_utils import send_post_request
from signals_utils.signals.mongo import signals, connector
from xml_utils.xsd_tree.xsd_tree import XSDTree

LOGGER = logging.getLogger(__name__)


def init():
    """ Connect to Data object events.
    """
    connector.connect(set_data_pid, signals.pre_save, sender=Data)


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
    default_system = list(ID_PROVIDER_SYSTEMS.keys())[0]

    pid_xpath = get_xpath_from_dot_notation(PID_XPATH)

    # Retrieve namespaces
    xml_tree = XSDTree.build_tree(document.xml_content)
    pid_xpath, namespaces = get_xpath_with_target_namespace(
        pid_xpath, document.template.content
    )

    # If PID XPath not found in document, do not go further
    try:
        document_pid = get_value_at_xpath(xml_tree, pid_xpath, namespaces)
    except AssertionError:
        return

    pid_generation_url = "%s%s" % (
        SERVER_URI,
        reverse(
            "core_linked_records_app_rest_provider_record_view",
            kwargs={
                "provider": default_system,
                "record": ID_PROVIDER_PREFIX
            }
        )
    )

    # Generate new PID if none has been specified
    if document_pid is None or document_pid == "" or \
            re.match(r"^%s/?$" % pid_generation_url, document_pid) is not None:
        document_pid = pid_generation_url
    else:  # PID has been specified
        # Check that PID is following default format
        if re.match(r"^%s/%s$" % (pid_generation_url, PID_FORMAT), document_pid) is None:
            raise exceptions.ModelError("Invalid PID provided")

        # Check that PID is not assigned to another document
        # * Check 1: document is already registered in database
        if document.pk is not None \
                and not system_api.is_pid_defined_for_document(document_pid, document.pk) \
                and system_api.is_pid_defined(document_pid):
            raise exceptions.ModelError("PID already defined for another document")

        # * Check 2: registering a new document in the database
        if document.pk is None and system_api.is_pid_defined(document_pid):
            raise exceptions.ModelError("PID already defined for another document")

    # Register the PID and return the URL provided
    document_pid_response = send_post_request(
        "%s?format=json" % document_pid
    )
    document_pid = document_pid_response.json()["url"]

    # Set the document PID into XML data and update `xml_content`
    set_value_at_xpath(xml_tree, pid_xpath, document_pid, namespaces)
    document.xml_content = XSDTree.tostring(xml_tree)

    # Update the whole document with the updated XML content
    document.convert_to_file()
    document.convert_to_dict()
