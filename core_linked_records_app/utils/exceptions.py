""" Exceptions for core_linked_records_app.
"""
from core_main_app.commons.exceptions import CoreError


class PidCreateError(CoreError):
    """Exception raised while creating a PID."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)


class PidResolverError(CoreError):
    """Exception raised when resolving a PID."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)


class InvalidProviderError(CoreError):
    """Exception raised when a provider is not valid."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)


class InvalidPidError(CoreError):
    """Exception raised when a PID is not valid."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)


class InvalidPrefixError(CoreError):
    """Exception raised if an invalid prefix is detected."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)


class InvalidRecordError(CoreError):
    """Exception raised if an invalid record is detected."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message (str): Error message
        """
        super().__init__(message)
