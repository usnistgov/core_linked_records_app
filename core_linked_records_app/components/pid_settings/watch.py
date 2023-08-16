""" Initialization function for PID Settings
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)

logger = logging.getLogger(__name__)


def init():
    """Main initialization function"""
    try:
        if not PidSettings.get():
            pid_settings = PidSettings(auto_set_pid=settings.AUTO_SET_PID)
            pid_settings_system_api.upsert(pid_settings)
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Impossible to initialize PidSettings: %s", str(exc))
