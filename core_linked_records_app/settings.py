""" Core linked records app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")

PID_XPATH = getattr(settings, "PID_XPATH", "Resource.@localid")

ID_PROVIDER_SYSTEMS = getattr(settings, "ID_PROVIDER_SYSTEMS", {
    "local": {
        "class":
            "core_linked_records_app.utils.providers.local.LocalIdProvider",
        "args": [
            SERVER_URI
        ]
    }
})
