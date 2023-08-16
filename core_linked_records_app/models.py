"""Linked records models
"""
from django.db import models

from core_linked_records_app.access_control import rights
from core_main_app.permissions.utils import get_formatted_name


class LinkedRecords(models.Model):
    """LinkedRecords"""

    class Meta:
        """Meta"""

        verbose_name = rights.APP_CONTENT_TYPE
        default_permissions = ()
        permissions = (
            (
                rights.CAN_READ_PID_SETTINGS,
                get_formatted_name(rights.CAN_READ_PID_SETTINGS),
            ),
        )
