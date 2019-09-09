""" Core linked records app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")

HANDLE_SYSTEMS = getattr(settings, "HANDLE_SYSTEMS", {})

