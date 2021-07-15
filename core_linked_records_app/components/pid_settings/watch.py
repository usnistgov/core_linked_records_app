""" Initialization function for PID Settings
"""
from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.components.pid_settings.models import PidSettings


def init():
    if not PidSettings.get():
        pid_settings = PidSettings(auto_set_pid=settings.AUTO_SET_PID)
        pid_settings_api.upsert(pid_settings)
