""" Utilities related to PID
"""
import re

from core_linked_records_app import settings
from core_linked_records_app.utils.exceptions import (
    InvalidPrefixError,
    InvalidRecordError,
)
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


def get_pid_settings_dict(pid_setting) -> dict:
    """Retrieve all settings related to PID configuration and returns a dictionary.

    Args:
        pid_setting: PidSettings object from DB.

    Returns:
         Dictionary containing all PID settings in DB or configuration files.
    """
    return {
        "auto_set_pid": pid_setting.auto_set_pid,
        "path": settings.PID_PATH,
        "format": settings.PID_FORMAT,
        "system_name": settings.ID_PROVIDER_SYSTEM_NAME,
        "system_type": settings.ID_PROVIDER_SYSTEM_CONFIG["class"],
        "prefixes": settings.ID_PROVIDER_PREFIXES,
    }


def split_prefix_from_record(record):
    """Split prefix from record if the record is in prefix/record format.

    Args:
        record (str): The full prefix/record_name to be split

    Raises:
        InvalidPrefixError: If an undefined prefix is detected.
        InvalidRecordError: If the record does not match the expected format.

    Returns:
        tuple[str, str|None] - prefix / record
    """
    prefix_record_list = record.split("/")

    if len(prefix_record_list) == 1:  # No record provided
        prefix = prefix_record_list[0]
        record = None
    elif prefix_record_list[-1] == "":  # Only prefix provided
        prefix = "/".join(prefix_record_list[:-1])
        record = None
    else:  # Prefix and record provided
        prefix = "/".join(prefix_record_list[:-1])
        record = prefix_record_list[-1]

    # Assign default prefix if the prefix is undefined or not in the
    # list of authorized ones.
    if prefix == "" or prefix not in settings.ID_PROVIDER_PREFIXES:
        raise InvalidPrefixError(f"Prefix {prefix} is not valid.")

    if (
        record is not None
        and record != ""
        and re.match(f"^({settings.PID_FORMAT}|)$", record) is None
    ):
        raise InvalidRecordError(f"Record {record} is not valid.")

    return prefix, record
