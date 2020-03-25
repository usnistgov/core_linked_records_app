""" Signals to trigger before Data save
"""
import logging
import re

from django.urls import reverse

from core_linked_records_app.settings import ID_PROVIDER_SYSTEMS, PID_XPATH, SERVER_URI, \
    ID_PROVIDER_PREFIX
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils.xml import get_xpath_from_dot_notation, \
    get_xpath_with_target_namespace, get_value_at_xpath, set_value_at_xpath
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

    # Retrieve element value
    try:
        document_pid = get_value_at_xpath(xml_tree, pid_xpath, namespaces)
    except AssertionError:  # PID XPath not found in document
        return

    # Decide if the PID needs to be generated
    generate_pid = True

    if document_pid is not None and document_pid != "" and document.pk is not None:
        try:
            generate_pid = not system_api.is_pid_defined_for_document(
                document_pid, document.pk
            )
        except Exception as e:
            LOGGER.info("Exception when fetching local id %s: %s" % (
                document_pid, str(e)
            ))

    if generate_pid:  # If the PID needs to be generated
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

        # If the document PID is not a valid PID URL, generate a random PID
        if re.match(r"^%s/[a-zA-Z0-9_\-]+$" % pid_generation_url, document_pid) is None:
            document_pid = pid_generation_url

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
