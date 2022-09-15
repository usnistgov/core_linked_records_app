""" Utilities related to PID
"""
import re
from django.urls import reverse

from core_linked_records_app import settings


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

    # Build regexp and test if it matches the pid_value
    pid_regexp_match = reverse(
        "core_linked_records_provider_record",
        kwargs={
            "provider": pid_provider_name,
            "record": "@format@",
        },
    ).replace("@format@", pid_format)

    return (
        re.match(pid_regexp_match, pid_value.replace(settings.SERVER_URI, ""))
        is not None
    )
