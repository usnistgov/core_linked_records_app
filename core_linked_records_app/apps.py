""" Apps file for setting linked records when app is ready
"""
import sys

from django.apps import AppConfig

from core_linked_records_app.components.data import watch as data_watch
from core_linked_records_app.settings import AUTO_SET_PID


class LinkedRecordsAppConfig(AppConfig):
    """Core application settings"""

    name = "core_linked_records_app"

    def ready(self):
        """Run when the app is ready

        Returns:

        """
        if "migrate" not in sys.argv:
            if AUTO_SET_PID:
                data_watch.init()
