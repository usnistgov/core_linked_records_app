""" Signals to trigger before Data save
"""
import logging
from os.path import join

from django.db.models.signals import pre_save

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils import data as data_utils
from core_linked_records_app.utils.xml import (
    get_xpath_from_dot_notation,
    get_xpath_with_target_namespace,
)

logger = logging.getLogger(__name__)


def init():
    """Connect to Data object events."""
    pre_save.connect(set_data_pid, sender=Data)


def set_data_pid(sender, instance, **kwargs):
    """Set the PID in the XML field specified in the settings. If the PID
    already exists and is valid, it is not reset.

    Params:
        sender:
        instance:
        kwargs:

    Returns:
    """
    from core_linked_records_app.utils import providers as providers_utils

    try:
        if not pid_settings_api.get().auto_set_pid:
            return

        # Retrieve PID XPath from `PidSettings.xpath_list`. Skip PID assignment
        # if the PID XPath is not defined for the template.
        template_pid_xpath = system_api.get_pid_xpath_by_template(instance.template)
        pid_xpath = get_xpath_with_target_namespace(
            get_xpath_from_dot_notation(template_pid_xpath.xpath),
            instance.template.content,
        )

        try:  # Retrieve the PID located at predefined XPath
            pid_value = data_utils.get_pid_value_for_data(instance, pid_xpath)
        except Exception as exc:  # XPath is not valid for current instance
            logger.warning(
                "Cannot create PID at %s for data %s: %s",
                pid_xpath,
                instance.pk,
                str(exc),
            )
            return

        # Remove previous instance PID from DB.
        if instance.pk is not None:
            system_api.delete_pid_for_data(instance)

        provider_name = providers_utils.retrieve_provider_name(pid_value)

        # Assign default value for undefined PID and check that the PID is not
        # defined for a instance other than the current instance.
        if pid_value is None or pid_value == "":
            pid_value = join(
                providers_utils.ProviderManager()
                .get(provider_name)
                .provider_lookup_url,
                settings.ID_PROVIDER_PREFIX_DEFAULT,
            )

        if system_api.is_pid_defined(pid_value) and (
            instance.pk is None
            or not system_api.is_pid_defined_for_data(pid_value, instance.pk)
        ):
            raise exceptions.ModelError("PID already defined for another instance")

        # Register PID and write resulting URL in instance
        pid_value = providers_utils.register_pid_for_data_id(
            provider_name, pid_value, instance.pk
        )
        data_utils.set_pid_value_for_data(instance, pid_xpath, pid_value)
    except exceptions.ModelError as model_error:
        logger.error("An error occurred while assigning PID: %s", str(model_error))
        raise exceptions.ModelError(str(model_error))
    except Exception as exc:
        if not instance.pk:
            data_definition = "new data"
        else:
            data_definition = f"data '{instance.pk}'"

        error_message = f"An error occurred while assigning PID to {data_definition}"

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.CoreError(f"{error_message}.")
