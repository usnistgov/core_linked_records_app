""" API for PidSettings model
"""
from core_linked_records_app.components.pid_settings.models import PidSettings


def upsert(pid_settings_object):
    """Insert or update the PidSettings provided as parameter.

    Args:
        pid_settings_object:

    Returns:
        Saved PidSettings object
    """
    return pid_settings_object.save()


def get():
    """Retrieve the PidSettings object from DB.

    Returns:
        PidSettings object
    """
    return PidSettings.get()
