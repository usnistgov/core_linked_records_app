""" Signals to trigger after Blob modificaations.
"""
import json
from logging import getLogger

from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.urls import resolve, Resolver404
from rest_framework import status

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.blob import api as blob_system_api
from core_linked_records_app.utils import exceptions
from core_linked_records_app.utils.pid import split_prefix_from_record
from core_linked_records_app.utils.providers import ProviderManager
from core_main_app.commons.exceptions import CoreError, DoesNotExist
from core_main_app.components.blob.models import Blob

logger = getLogger(__name__)


def init():
    """Connect to Blob object events."""
    post_save.connect(set_blob_pid, sender=Blob)
    post_delete.connect(delete_blob_pid, sender=Blob)


def _register_pid_for_blob_id(provider_name, pid_value, blob_id):
    """Registers a blob with a set PID to a given provider.

    Args:
        provider_name:
        pid_value:
        blob_id:

    Returns:
        str - Persistent identifier
    """
    # Retrieve provider, prefix and record information to register the blob in
    # the default provider.
    try:
        # Retrieve the current provider.
        provider_manager = ProviderManager()
        provider = provider_manager.get(provider_name)
    except Exception as exc:
        error_message = (
            "Error while retrieving the provider for registring the PID"
        )
        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.InvalidProviderError(error_message)

    # Parse the `pid_value` to obtain record & prefix info.
    local_pid_url = pid_value.replace(
        provider.provider_lookup_url, provider.local_url
    )

    # Try resolving the `local_pid_url` and ensure the expected view was
    # retrieved.
    try:
        resolver_match = resolve(
            local_pid_url.replace(settings.SERVER_URI, "")
        )

        if resolver_match.view_name != "core_linked_records_provider_record":
            raise Resolver404()
    except Resolver404 as exc:
        error_message = "Invalid view retrieved while registring the PID"
        logger.error(error_message)
        raise exceptions.PidResolverError(error_message) from exc

    # Before asking the provider to create a record, separate prefix from
    # record name.
    try:
        prefix, record = split_prefix_from_record(
            resolver_match.kwargs["record"]
        )
    except (
        exceptions.InvalidPrefixError,
        exceptions.InvalidRecordError,
    ) as exc:
        error_message = "Error while retrieving prefix from the PID record"
        logger.error("%s: %s", error_message, str(exc))
        raise exceptions.InvalidPidError(error_message)

    provider_response = provider.create(prefix, record)

    # If an error happened during PID registration, try to relay the message
    # from the provider, otherwise relay a default error message.
    default_error_message = "An error occurred while creating the PID"
    try:
        if (
            provider_response.status_code
            not in [status.HTTP_200_OK, status.HTTP_201_CREATED]
            and blob_system_api.get_blob_by_pid(pid_value).pk != blob_id
        ):
            error_message = json.loads(provider_response.content).get(
                "message", default_error_message
            )
            logger.error(error_message)
            raise exceptions.PidCreateError(error_message)
    except Exception as exc:  # If the response is not JSON parsable
        logger.error("%s: %s", default_error_message, str(exc))
        raise exceptions.PidCreateError(default_error_message)

    return json.loads(provider_response.content)["url"]


def _set_blob_pid(instance: Blob):
    """Set the PID in the given Blob `instance`. If the PID
    already exists and is valid, it is not reset.

    Args:
        instance:

    Raises:
        CoreError: If any exception occur while executing the function.
    """
    try:
        if not PidSettings.get().auto_set_pid:
            return

        try:
            blob_system_api.get_pid_for_blob(str(instance.pk))
        except DoesNotExist:
            # Create default PID value.
            default_pid_value = (
                f"{ProviderManager().get(settings.ID_PROVIDER_SYSTEM_NAME).provider_lookup_url}/"
                f"{settings.ID_PROVIDER_PREFIX_DEFAULT}"
            )

            # Register PID and write resulting URL in instance.
            pid_value = _register_pid_for_blob_id(
                settings.ID_PROVIDER_SYSTEM_NAME,
                default_pid_value,
                instance.pk,
            )
            blob_system_api.set_pid_for_blob(instance.pk, pid_value)
    except Exception as exc:
        error_message = (
            f"An error occurred while setting a PID for blob '{instance.pk}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise CoreError(f"{error_message}.") from exc


def set_blob_pid(
    sender, instance: Blob, **kwargs  # noqa, pylint: disable=unused-argument
):
    """Wrapper around `_set_blob_pid` to ensure the PID can be updated while
    the Blob is being saved without locking the DB.

    Args:
        sender:
        instance:
        kwargs:
    """
    transaction.on_commit(lambda: _set_blob_pid(instance))


def delete_blob_pid(
    sender, instance: Blob, **kwargs  # noqa, pylint: disable=unused-argument
):
    """Delete a PID assigned to a Blob

    Args:
        sender:
        instance:
        kwargs:
    """
    try:
        blob_system_api.delete_pid_for_blob(instance)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning(
            "Trying to delete PID for blob %d (%s) but an error occurred: %s",
            instance.pk,
            instance.filename,
            str(exc),
        )
