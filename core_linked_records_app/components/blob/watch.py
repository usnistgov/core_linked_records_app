""" Signals to trigger after Blob save
"""
import json
from logging import getLogger

from django.db.models.signals import post_save
from django.urls import reverse

from core_main_app.commons.exceptions import CoreError, DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.utils.requests_utils.requests_utils import send_post_request
from core_linked_records_app import settings
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.pid_settings import api as pid_settings_api

logger = getLogger(__name__)


def init():
    """Connect to Blob object events."""
    post_save.connect(set_blob_pid, sender=Blob)


def set_blob_pid(sender, instance, **kwargs):
    """set_blob_pid

    Args:
        sender:
        instance:

    Returns:

    """
    try:
        if not pid_settings_api.get().auto_set_pid:
            return

        try:
            blob_api.get_pid_for_blob(str(instance.pk))
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

            blob_api.set_pid_for_blob(instance.pk, blob_pid)
    except Exception as exc:
        error_message = (
            f"An error occurred while setting a PID for blob '{instance.pk}'"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise CoreError(f"{error_message}.")
