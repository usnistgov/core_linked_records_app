""" Signals to trigger after Blob save
"""
from logging import getLogger

import json
from django.urls import reverse

from core_linked_records_app import settings
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_main_app.commons.exceptions import CoreError, DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.utils.requests_utils.requests_utils import send_post_request
from signals_utils.signals.mongo import connector, signals

logger = getLogger(__name__)


def init():
    """Connect to Blob object events."""
    connector.connect(set_blob_pid, signals.post_save, sender=Blob)


def set_blob_pid(sender, document, **kwargs):
    try:
        if not pid_settings_api.get().auto_set_pid:
            return

        try:
            blob_api.get_pid_for_blob(str(document.id))
        except DoesNotExist:
            # Register new PID for the saved Blob.
            sub_url = reverse(
                "core_linked_records_provider_record",
                kwargs={
                    "provider": settings.DEFAULT_ID_PROVIDER_SYSTEM,
                    "record": settings.ID_PROVIDER_PREFIX_BLOB,
                },
            )
            pid_response = send_post_request(
                f"{settings.SERVER_URI}{sub_url}?format=json"
            )
            blob_pid = json.loads(pid_response.content)["url"]

            blob_api.set_pid_for_blob(document.id, blob_pid)
    except Exception as exc:
        error_message = (
            f"An error occurred while setting a PID for blob '{document.id}'"
        )

        logger.error(f"{error_message}: {str(exc)}")
        raise CoreError(f"{error_message}.")
