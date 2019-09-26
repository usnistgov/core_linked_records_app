""" Core linked records app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")

PID_XPATH = getattr(settings, "PID_XPATH", "Resource.@localid")

HANDLE_SYSTEMS = getattr(settings, "HANDLE_SYSTEMS", {})

