""" Signals to trigger after Blob modificaations.
"""
import json
from logging import getLogger

from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.urls import reverse

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.blob import api as blob_system_api
from core_main_app.commons.exceptions import CoreError, DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.utils.requests_utils.requests_utils import send_post_request

logger = getLogger(__name__)


def init():
    """Connect to Blob object events."""
    post_save.connect(set_blob_pid, sender=Blob)
    post_delete.connect(delete_blob_pid, sender=Blob)


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
            # Register new PID for the saved Blob.
            sub_url = reverse(
                "core_linked_records_provider_record",
                kwargs={
                    "provider": settings.ID_PROVIDER_SYSTEM_NAME,
                    "record": settings.ID_PROVIDER_PREFIX_BLOB,
                },
            )
            pid_response = send_post_request(
                f"{settings.SERVER_URI}{sub_url}?format=json"
            )
            blob_pid = json.loads(pid_response.content)["url"]

            blob_system_api.set_pid_for_blob(instance.pk, blob_pid)
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
