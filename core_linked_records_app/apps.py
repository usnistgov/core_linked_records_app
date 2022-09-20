""" Apps file for setting linked records when app is ready
"""
import sys

from django.apps import AppConfig


class LinkedRecordsAppConfig(AppConfig):
    """Core application settings"""

    name = "core_linked_records_app"
    verbose_name = "Core Linked Records App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        from core_main_app.commons.exceptions import CoreError
        from core_linked_records_app import settings
        from core_linked_records_app.components.blob import watch as blob_watch
        from core_linked_records_app.components.data import watch as data_watch
        from core_linked_records_app.components.pid_settings import (
            watch as pid_settings_watch,
        )

        if "" in settings.ID_PROVIDER_PREFIXES:
            raise CoreError(
                "Empty string not allowed in settings.ID_PROVIDER_PREFIXES."
            )

        if "migrate" not in sys.argv:
            pid_settings_watch.init()
            data_watch.init()
            blob_watch.init()
