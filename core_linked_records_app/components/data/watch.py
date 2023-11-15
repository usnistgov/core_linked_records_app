""" Signals to trigger before Data save
"""
import json
import logging

from django.db import transaction
from django.db.models.signals import pre_save, post_delete
from django.urls import resolve
from rest_framework import status

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.data import api as data_system_api
from core_linked_records_app.system.pid_path import (
    api as pid_path_system_api,
)
from core_linked_records_app.utils import data as data_utils
from core_linked_records_app.utils import exceptions
from core_linked_records_app.utils.pid import split_prefix_from_record
from core_linked_records_app.utils.providers import (
    ProviderManager,
    retrieve_provider_name,
)
from core_main_app.components.data.models import Data

logger = logging.getLogger(__name__)


def init():
    """Connect to Data object events."""
    pre_save.connect(set_data_pid, sender=Data)
    post_delete.connect(delete_data_pid, sender=Data)


def _register_pid_for_data_id(provider_name, pid_value, data_id):
    """Registers a data with a set PID to a given provider.

    Args:
        provider_name:
        pid_value:
        data_id:

    Returns:
        str - Persistent identifier
    """
    # Retrieve provider, prefix and record information to register the record in
    # the default provider.
    try:
        # Retrieve the current provider.
        provider_manager = ProviderManager()
        provider = provider_manager.get(provider_name)

        # Parse the `pid_value` to obtain record & prefix info.
        local_pid_url = pid_value.replace(
            provider.provider_lookup_url, provider.local_url
        )

        # Try resolving the `local_pid_url` and ensure the expected view was
        # retrieved.
        resolver_match = resolve(
            local_pid_url.replace(settings.SERVER_URI, "")
        )
        assert (
            resolver_match.view_name == "core_linked_records_provider_record"
        )

        # Before asking the provider to create a record, separate prefix from
        # record name.
        prefix, record = split_prefix_from_record(
            resolver_match.kwargs["record"]
        )
    except Exception as exc:
        error_message = (
            "An unexpected error occurred while retrieving information to "
            "register the PID"
        )
        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.PidResolverError(f"{error_message}.")

    provider_response = provider.create(prefix, record)

    # If an error happened during PID registration, try to relay the message
    # from the provider, otherwise relay a default error message.
    if (
        provider_response.status_code != status.HTTP_201_CREATED
        and provider_response.status_code != status.HTTP_200_OK
        and data_system_api.get_data_by_pid(pid_value).pk != data_id
    ):
        default_error_message = "An error occurred while creating the PID"
        try:
            error_message = json.loads(provider_response.content).get(
                "message", default_error_message
            )
            logger.error(error_message)
            raise exceptions.PidCreateError(error_message)
        except Exception as exc:  # If the response is not JSON parsable
            logger.error("%s: %s", default_error_message, str(exc))
            raise exceptions.PidCreateError(default_error_message)

    return json.loads(provider_response.content)["url"]


def _set_data_pid(instance: Data):
    """Set the PID in the field specified in the settings. If the PID
    already exists and is valid, it is not reset.

    Args:
        instance:

    Returns:
    """
    try:
        if not PidSettings.get().auto_set_pid:
            return

        # Retrieve PID path from `PidSettings.path_list`. Skip PID assignment
        # if the PID path is not defined for the template.
        template_pid_path = pid_path_system_api.get_pid_path_by_template(
            instance.template
        )
        pid_path = template_pid_path.path

        try:  # Retrieve the PID located at predefined dot notation path.
            pid_value = data_utils.get_pid_value_for_data(instance, pid_path)
        except Exception as exc:  # pylint: disable=broad-except
            # PID path is not valid for current instance.
            logger.warning(
                "Cannot create PID at %s for data %s: %s",
                pid_path,
                instance.pk,
                str(exc),
            )
            return

        # Remove previous instance PID from DB.
        if instance.pk is not None:
            transaction.on_commit(
                lambda: data_system_api.delete_pid_for_data(instance)
            )

        provider_name = retrieve_provider_name(pid_value)

        # Assign default value for undefined PID and check that the PID is not
        # defined for a instance other than the current instance.
        if pid_value is None or pid_value == "":
            pid_value = (
                f"{ProviderManager().get(provider_name).provider_lookup_url}/"
                f"{settings.ID_PROVIDER_PREFIX_DEFAULT}"
            )

        if data_system_api.is_pid_defined(pid_value) and (
            instance.pk is None
            or not data_system_api.is_pid_defined_for_data(
                pid_value, instance.pk
            )
        ):
            raise exceptions.PidCreateError(
                "PID already defined for another instance"
            )

        # Register PID and write resulting URL in instance
        pid_value = _register_pid_for_data_id(
            provider_name, pid_value, instance.pk
        )
        data_utils.set_pid_value_for_data(instance, pid_path, pid_value)
    except exceptions.PidCreateError as pid_create_error:
        logger.error(
            "An error occurred while assigning PID: %s", str(pid_create_error)
        )
        raise exceptions.PidCreateError(str(pid_create_error))
    except Exception as exc:
        if not instance.pk:
            data_definition = "new data"
        else:
            data_definition = f"data '{instance.pk}'"

        error_message = (
            f"An error occurred while assigning PID to {data_definition}"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.PidCreateError(f"{error_message}.")


def set_data_pid(
    sender, instance: Data, **kwargs  # noqa, pylint: disable=unused-argument
):
    """Wrapper around `_set_data_pid` to ensure the PID can be updated while
    the Data is being saved without locking the DB.

    Args:
        sender:
        instance:
        kwargs:

    Returns:
    """
    transaction.on_commit(lambda: _set_data_pid(instance))


def delete_data_pid(
    sender, instance: Data, **kwargs  # noqa, pylint: disable=unused-argument
):
    """Delete a PID assigned to a Data

    Args:
        sender:
        instance:
        kwargs:
    """
    try:
        data_system_api.delete_pid_for_data(instance)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning(
            "Trying to delete PID for data %d but an error occurred: %s",
            instance.pk,
            str(exc),
        )
