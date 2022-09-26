""" Utilities related to PID
"""
import re

from core_linked_records_app import settings
from core_linked_records_app.utils.providers import ProviderManager


def is_valid_pid_value(pid_value, pid_provider_name, pid_format):
    """Check if a provided PID has a valid URL according to the provided settings

    Args:
        pid_value: str - Value of the PID
        pid_provider_name: str - Expected provider of the PID
        pid_format: str - Regexp format of the record

    Returns:
        bool - True if the PID matches the regexp, False otherwise.
    """
    if not pid_value:  # Don't test if pid_value is None or ''
        return False

    # Retrieve the active provider
    provider = ProviderManager().get(pid_provider_name)

    # Build regexp and test if it matches the pid_value
    pid_prefixes_regexp = "|".join(settings.ID_PROVIDER_PREFIXES)
    pid_regexp_match = f"{provider.provider_lookup_url}/(?:{pid_prefixes_regexp})/{pid_format}"

    return re.match(pid_regexp_match, pid_value) is not None
