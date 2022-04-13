""" Core linked records app settings

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(
    settings,
    "INSTALLED_APPS",
    [],
)
SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")

PID_XPATH = getattr(settings, "PID_XPATH", "Resource.@localid")

PID_FORMAT = getattr(settings, "PID_FORMAT", r"[a-zA-Z0-9_\-]+")

ID_PROVIDER_SYSTEM_NAME = getattr(settings, "ID_PROVIDER_SYSTEM_NAME", "local")

ID_PROVIDER_SYSTEM_CONFIG = getattr(
    settings,
    "ID_PROVIDER_SYSTEM_CONFIG",
    {
        "class": "core_linked_records_app.utils.providers.local.LocalIdProvider",
        "args": [SERVER_URI],
    },
)

ID_PROVIDER_PREFIXES = getattr(settings, "ID_PROVIDER_PREFIXES", ["cdcs"])

ID_PROVIDER_PREFIX_DEFAULT = getattr(
    settings, "ID_PROVIDER_PREFIX_DEFAULT", ID_PROVIDER_PREFIXES[0]
)

ID_PROVIDER_PREFIX_BLOB = getattr(
    settings, "ID_PROVIDER_PREFIX_BLOB", ID_PROVIDER_PREFIXES[0]
)

HANDLE_NET_RECORD_INDEX = getattr(settings, "HANDLE_NET_RECORD_INDEX", 1)

HANDLE_NET_ADMIN_DATA = getattr(
    settings,
    "HANDLE_NET_ADMIN_DATA",
    {
        "index": 100,
        "type": "HS_ADMIN",
        "data": {
            "format": "admin",
            "value": {
                "handle": f"0.NA/{ID_PROVIDER_PREFIX_DEFAULT}",
                "index": 200,
                "permissions": "011111110011",
            },
        },
    },
)

AUTO_SET_PID = getattr(settings, "AUTO_SET_PID", False)
