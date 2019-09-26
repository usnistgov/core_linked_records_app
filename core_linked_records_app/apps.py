""" Apps file for setting linked records when app is ready
"""
from django.apps import AppConfig

from core_linked_records_app.components.data import watch as data_watch


class LinkedRecordsAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_linked_records_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        data_watch.init()
