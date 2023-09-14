""" Initialize permissions related to PID implementation.
"""
import logging

from core_linked_records_app.access_control import rights
from core_main_app.components.group import api as group_api
from core_main_app.permissions import (
    rights as main_rights,
    api as permissions_api,
)

logger = logging.getLogger(__name__)


def init_permissions():
    """Initialize groups and permissions."""
    try:
        # Get or create the default group
        default_group, _ = group_api.get_or_create(
            name=main_rights.DEFAULT_GROUP
        )

        can_read_pid_settings_perm = permissions_api.get_by_codename(
            codename=rights.CAN_READ_PID_SETTINGS
        )

        # Add permissions to default group.
        default_group.permissions.add(
            can_read_pid_settings_perm,
        )
    except Exception as exception:  # pylint: disable=broad-except
        logger.error(
            "Impossible to init permissions for core_linked_records_app: %s",
            str(exception),
        )
