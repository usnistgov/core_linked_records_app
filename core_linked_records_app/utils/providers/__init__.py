""" Handle system abstract class
"""

import logging
from abc import ABC, abstractmethod
from importlib import import_module

from django.urls import reverse
from rest_framework import status

from core_linked_records_app import settings
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import CoreError

logger = logging.getLogger(__name__)


class AbstractIdProvider(ABC):
    """Abstract Id Provider"""

    def __init__(self, provider_name, provider_lookup_url):
        core_linked_records_provider_records = reverse(
            "core_linked_records_provider_record",
            kwargs={"provider": provider_name, "record": ""},
        )
        self.local_url = (
            f"{settings.SERVER_URI}" f"{core_linked_records_provider_records}"
        )

        self.local_url = self.local_url[:-1]  # Removing the final /
        self.provider_lookup_url = (
            provider_lookup_url if provider_lookup_url else self.local_url
        )

    @abstractmethod
    def get(self, record):
        """get
        Args:
            record:
        """
        raise NotImplementedError()

    @abstractmethod
    def create(self, prefix, record=None):
        """create
        Args:
            prefix:
            record:
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, record):
        """update
        Args:
            record:
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, record):
        """delete
        Args:
            record:
        """
        raise NotImplementedError()


class ProviderManager:
    """Manage provider instances from a given provider name"""

    def __init__(self):
        self._provider_instance = None

        self.provider_name = settings.ID_PROVIDER_SYSTEM_NAME
        self.provider_config = settings.ID_PROVIDER_SYSTEM_CONFIG

    def get(self, provider_name=None) -> AbstractIdProvider:
        """get provider
        Args:
            provider_name:

        Returns:

        """
        if self._provider_instance is None:
            # Retrieve class name and module path
            id_provider_classpath = self.provider_config["class"].split(".")
            id_provider_classname = id_provider_classpath[-1]
            id_provider_modpath = ".".join(id_provider_classpath[:-1])

            # Import module and class
            id_provider_module = import_module(id_provider_modpath)
            id_provider_class = getattr(
                id_provider_module, id_provider_classname
            )

            # Initialize handle system instance, default to the system specified in
            # settings.
            if provider_name is None:
                provider_name = settings.ID_PROVIDER_SYSTEM_NAME

            self._provider_instance = id_provider_class(
                provider_name, *settings.ID_PROVIDER_SYSTEM_CONFIG["args"]
            )

        return self._provider_instance

    def find_provider_from_pid(self, pid):
        """find_provider_from_pid
        Args:
            pid:

        Returns:

        """
        provider = self.get(settings.ID_PROVIDER_SYSTEM_NAME)

        return (
            settings.ID_PROVIDER_SYSTEM_NAME
            if pid.startswith(provider.provider_lookup_url)
            else None
        )


def retrieve_provider_name(pid_value):
    """Retrieve name of the provider given a PID.

    Args:
        pid_value:

    Returns:
         str - Provider name
    """

    if pid_value is None or pid_value == "":  # PID field left blank
        # Select the default provider if no PID has been chosen.
        provider_name = settings.ID_PROVIDER_SYSTEM_NAME
    else:  # PID specified in document.
        provider_name = ProviderManager().find_provider_from_pid(pid_value)

    # Detect provider specified by PID. Raise an error if no matching providers are
    # found.
    if provider_name is None:
        raise exceptions.ModelError(
            "Invalid PID provided (provider not found)"
        )

    return provider_name


def delete_record_from_provider(record_name: str):
    """Delete a PID from the provider using the record name as stored in the
    LocalId table.

    Args:
        record_name: str - Formatted as prefix/record.

    Raises:
        ApiError: if the HTTP status is not 200 or 404.
    """
    # Delete the given LocalID fron the default PID provider.
    provider = ProviderManager().get()
    previous_pid_delete_response = provider.delete(record_name)

    if previous_pid_delete_response.status_code == status.HTTP_200_OK:
        return

    # At this point, there was some problem deleting the LocalID needed to be logged.
    error_message = (
        f"Deletion of LocalID {record_name} from provider "
        f"{ProviderManager().provider_name} returned "
        f"{previous_pid_delete_response.status_code}"
    )

    # Do not crash for a 404, but log that an error occured.
    if previous_pid_delete_response.status_code == status.HTTP_404_NOT_FOUND:
        logger.warning(error_message)
        return

    # Log any error that happened during PID deletion.
    logger.error(error_message)
    raise CoreError(error_message)
