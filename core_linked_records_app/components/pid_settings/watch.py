""" Initialization function for PID Settings
"""
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.settings import AUTO_SET_PID
from core_linked_records_app.components.pid_settings import api as pid_settings_api


def init():
    if not PidSettings.get():
        pid_settings = PidSettings(auto_set_pid=AUTO_SET_PID)
        pid_settings_api.upsert(pid_settings)
