""" Signals to trigger before Data save
"""
from os.path import join

import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils import data as data_utils
from core_linked_records_app.utils.xml import (
    get_xpath_from_dot_notation,
    get_xpath_with_target_namespace,
)
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from signals_utils.signals.mongo import signals, connector

logger = logging.getLogger(__name__)


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
    from core_linked_records_app.utils import providers as providers_utils

    try:
        if not pid_settings_api.get().auto_set_pid:
            return

        # Retrieve PID XPath from `PidSettings.xpath_list`. Skip PID assignment
        # if the PID XPath is not defined for the template.
        template_pid_xpath = system_api.get_pid_xpath_by_template_id(
            document.template.pk
        )
        pid_xpath = get_xpath_with_target_namespace(
            get_xpath_from_dot_notation(template_pid_xpath.xpath),
            document.template.content,
        )

        try:  # Retrieve the PID located at predefined XPath
            pid_value = data_utils.get_pid_value_for_data(document, pid_xpath)
        except Exception as exc:  # XPath is not valid for current document
            logger.warning(
                f"Cannot create PID at {pid_xpath} for data {document.pk}: {str(exc)}"
            )
            return

        # Remove previous document PID from DB.
        if document.pk is not None:
            system_api.delete_pid_for_data(document)

        provider_name = providers_utils.retrieve_provider_name(pid_value)

        # Assign default value for undefined PID and check that the PID is not
        # defined for a document other than the current document.
        if pid_value is None or pid_value == "":
            pid_value = join(
                providers_utils.ProviderManager().get(provider_name).provider_url,
                settings.ID_PROVIDER_PREFIX_DEFAULT,
            )

        if system_api.is_pid_defined(pid_value) and (
            document.pk is None
            or not system_api.is_pid_defined_for_document(pid_value, document.pk)
        ):
            raise exceptions.ModelError("PID already defined for another document")

        # Register PID and write resulting URL in document
        pid_value = providers_utils.register_pid_for_data_id(
            provider_name, pid_value, document.pk
        )
        data_utils.set_pid_value_for_data(document, pid_xpath, pid_value)
    except exceptions.ModelError as model_error:
        logger.error(f"An error occurred while assigning PID: {str(model_error)}")
        raise exceptions.ModelError(str(model_error))
    except Exception as exc:
        if not document.id:
            data_definition = "new data"
        else:
            data_definition = f"data '{document.id}'"

        error_message = f"An error occurred while assigning PID to {data_definition}"

        logger.error(f"{error_message}: {str(exc)}")
        raise exceptions.CoreError(f"{error_message}.")
