""" API for PidSettings model
"""
import logging

from core_main_app.commons.exceptions import ApiError
from core_linked_records_app.components.pid_settings.models import PidSettings

logger = logging.getLogger(__name__)


def upsert(pid_settings_object):
    """Insert or update the PidSettings provided as parameter.

    Args:
        pid_settings_object:

    Returns:
        Saved PidSettings object
    """
    try:
        pid_settings_object.save()
        return pid_settings_object
    except Exception as exc:
        error_message = "An unexpected error occurred while saving PidSettings"

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.")


def get():
    """Retrieve the PidSettings object from DB.

    Returns:
        PidSettings object
    """
    try:
        return PidSettings.get()
    except Exception as exc:
        error_message = "An unexpected error occurred while retrieving PidSettings"

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(f"{error_message}.")
