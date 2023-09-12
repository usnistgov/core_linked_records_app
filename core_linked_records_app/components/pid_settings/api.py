""" Protected API to manage PidSettings object.
"""
import logging

from core_linked_records_app.components.pid_settings.access_control import (
    can_get_pid_settings,
    can_upsert_pid_settings,
)
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)
from core_main_app.access_control.decorators import access_control

logger = logging.getLogger(__name__)


@access_control(can_upsert_pid_settings)
def upsert(pid_settings_object, user):  # noqa, pylint: disable=unused-argument
    """Insert or update the PidSettings provided as parameter.

    Args:
        pid_settings_object:

    Returns:
        Saved PidSettings object
    """
    return pid_settings_system_api.upsert(pid_settings_object)


@access_control(can_get_pid_settings)
def get(user):  # noqa, pylint: disable=unused-argument
    """Retrieve the PidSettings object from DB.

    Returns:
        PidSettings object
    """
    return pid_settings_system_api.get()
