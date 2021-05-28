""" Signals to trigger before Data save
"""
from os.path import join

import logging
from rest_framework import status
from rest_framework.status import HTTP_200_OK

from core_linked_records_app import settings
from core_linked_records_app.settings import (
    PID_XPATH,
)
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils.providers import ProviderManager
from core_linked_records_app.utils.xml import (
    get_xpath_from_dot_notation,
    get_xpath_with_target_namespace,
    get_value_at_xpath,
    set_value_at_xpath,
)
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.utils.requests_utils.requests_utils import (
    send_post_request,
    send_delete_request,
)
from signals_utils.signals.mongo import signals, connector
from xml_utils.xpath import create_tree_from_xpath
from xml_utils.xsd_tree.xsd_tree import XSDTree
from core_linked_records_app.components.pid_settings import api as pid_settings_api

LOGGER = logging.getLogger(__name__)


def init():
    """Connect to Data object events."""
    connector.connect(set_data_pid, signals.pre_save, sender=Data)


def set_data_pid(sender, document, **kwargs):
    """Set the PID in the XML field specified in the settings. If the PID
    already exists and is valid, it is not reset.

    Params:
        sender:
        document:
        kwargs:

    Returns:
    """
    if not pid_settings_api.get().auto_set_pid:
        return

    pid_xpath = get_xpath_from_dot_notation(PID_XPATH)

    # Retrieve namespaces
    xml_tree = XSDTree.build_tree(document.xml_content)
    pid_xpath, namespaces = get_xpath_with_target_namespace(
        pid_xpath, document.template.content
    )

    try:  # Get the PID from the `pid_xpath` value
        document_pid = get_value_at_xpath(xml_tree, pid_xpath, namespaces)
        if type(document_pid) == str and document_pid.endswith(
            "/"
        ):  # Cleanup PID if it ends with a '/'
            document_pid = document_pid[:-1]
    except AssertionError:  # PID XPath not found in document
        try:  # Try to create the element at the given PID
            # Import libs that need to wait for apps to be ready
            from core_main_app.components.data import api as data_api

            modified_xml_tree = create_tree_from_xpath(pid_xpath, xml_tree, namespaces)
            set_value_at_xpath(
                modified_xml_tree, pid_xpath, "http://sample_pid.org", namespaces
            )
            document.xml_content = XSDTree.tostring(modified_xml_tree)
            data_api.check_xml_file_is_valid(document)

            # Replace the current by the modified tree (containing mock PID) and
            # force document PID to be regenerated.
            xml_tree = modified_xml_tree
            document_pid = None
        except Exception as exc:  # Cannot create PID at given XPath
            LOGGER.warning("Cannot create PID at %s: %s" % (pid_xpath, str(exc)))
            return

    # Identify provider name for registration and ensure the PID has not been
    # already defined in another document.
    provider_manager = ProviderManager()

    # Retrieve previous PID and remove it from DB.
    if document.pk is not None:
        previous_pid = system_api.get_pid_for_data(document.pk)

        previous_provider_name = provider_manager.find_provider_from_pid(previous_pid)
        previous_provider = provider_manager.get(previous_provider_name)
        previous_pid_url = previous_pid.replace(
            previous_provider.provider_url, previous_provider.local_url
        )

        previous_pid_delete_response = send_delete_request(
            "%s?format=json" % previous_pid_url
        )

        # Log any error that happen during PID deletion
        if previous_pid_delete_response.status_code != HTTP_200_OK:
            LOGGER.warning(
                "Deletion of PID %s returned %s"
                % (previous_pid, previous_pid_delete_response.status_code)
            )

    if document_pid is None or document_pid == "":  # PID field left blank
        # Select the default provider if no PID has been chosen.
        provider_name = list(settings.ID_PROVIDER_SYSTEMS.keys())[0]
        document_pid = join(
            provider_manager.get(provider_name).provider_url,
            settings.ID_PROVIDER_PREFIX_DEFAULT,
        )
    else:  # PID specified in document.
        # Check that the PID is not defined for a document other than the current
        # document.
        if system_api.is_pid_defined(document_pid) and (
            document.pk is None
            or not system_api.is_pid_defined_for_document(document_pid, document.pk)
        ):
            raise exceptions.ModelError("PID already defined for another document")

        provider_name = provider_manager.find_provider_from_pid(document_pid)

    # PID specified but not matching any possible provider URLs for the
    # generation.
    if provider_name is None:
        raise exceptions.ModelError("Invalid PID provided")

    provider = provider_manager.get(provider_name)
    registration_url = document_pid.replace(provider.provider_url, provider.local_url)

    document_pid_response = send_post_request("%s?format=json" % registration_url)

    if document_pid_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        default_error_message = "An error occurred while creating the PID"
        try:
            raise exceptions.ModelError(
                document_pid_response.json().get("message", default_error_message)
            )
        except ValueError:  # If the response is not JSON parsable
            raise exceptions.ModelError(default_error_message)

    if (
        document_pid_response.status_code != status.HTTP_201_CREATED
        and document_pid_response.status_code != status.HTTP_200_OK
        and system_api.get_data_by_pid(document_pid).pk != document.pk
    ):
        raise exceptions.ModelError("Invalid PID provided")

    # FIXME assert the value is not changed when saving
    document_pid = document_pid_response.json()["url"]

    # Set the document PID into XML data and update `xml_content`
    set_value_at_xpath(xml_tree, pid_xpath, document_pid, namespaces)
    document.xml_content = XSDTree.tostring(xml_tree)

    # Update the whole document with the updated XML content
    document.convert_to_file()
    document.convert_to_dict()
