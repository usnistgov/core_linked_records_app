""" Handle system abstract class
"""

import logging
from abc import ABC, abstractmethod
from importlib import import_module

from django.urls import reverse
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.utils.requests_utils.requests_utils import send_post_request
from core_linked_records_app import settings

logger = logging.getLogger(__name__)


class AbstractIdProvider(ABC):
    """Abstract Id Provider"""

    def __init__(
        self,
        provider_name,
        provider_lookup_url,
        provider_registration_url,
        username,
        password,
    ):

        self.local_url = (
            f"{settings.SERVER_URI}"
            f'{reverse("core_linked_records_provider_record",kwargs = {"provider": provider_name, "record": ""})}'
        )

        self.local_url = self.local_url[:-1]  # Removing the final /
        self.provider_lookup_url = (
            provider_lookup_url if provider_lookup_url else self.local_url
        )
        self.provider_registration_url = provider_registration_url
        self.auth_token = self.encode_token(username, password)

    @abstractmethod
    def encode_token(self, username, password):
        """encode_token
        Args:
            username:
            password:
        """
        raise NotImplementedError()

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

    def get(self, provider_name):
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
            id_provider_class = getattr(id_provider_module, id_provider_classname)

            # Initialize handel system instance
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
        raise exceptions.ModelError("Invalid PID provided (provider not found)")

    return provider_name


def register_pid_for_data_id(provider_name, pid_value, data_id):
    """Registers a data with a set PID to a given provider.

    Args:
        provider_name:
        pid_value:
        data_id:

    Returns:
        str - Persistent identifier
    """
    from core_linked_records_app.system import api as system_api

    provider_manager = ProviderManager()
    provider = provider_manager.get(provider_name)
    registration_url = pid_value.replace(
        provider.provider_lookup_url, provider.local_url
    )

    document_pid_response = send_post_request(f"{registration_url}?format=json")

    # If an error happened during PID registration, try to relay the message from the
    # provider, otherwise relay a default error message.
    if document_pid_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        default_error_message = "An error occurred while creating the PID"
        try:
            raise exceptions.ModelError(
                document_pid_response.json().get("message", default_error_message)
            )
        except Exception as exc:  # If the response is not JSON parsable
            logger.error("%s: %s", default_error_message, str(exc))
            raise exceptions.ModelError(default_error_message)

    if (
        document_pid_response.status_code != status.HTTP_201_CREATED
        and document_pid_response.status_code != status.HTTP_200_OK
        and system_api.get_data_by_pid(pid_value).pk != data_id
    ):
        raise exceptions.ModelError("Invalid PID provided")

    return document_pid_response.json()["url"]
