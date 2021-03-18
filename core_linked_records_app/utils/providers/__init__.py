""" Handle system abstract class
"""
from abc import ABC, abstractmethod
from importlib import import_module

from django.urls import reverse

from core_linked_records_app import settings


class AbstractIdProvider(ABC):
    def __init__(self, provider_name, provider_url, username, password):
        self.provider_url = provider_url
        self.local_url = "%s%s" % (
            settings.SERVER_URI,
            reverse(
                "core_linked_records_provider_record",
                kwargs={"provider": provider_name, "record": ""},
            ),
        )
        self.local_url = self.local_url[:-1]  # Removing the final /
        self.auth_token = self.encode_token(username, password)

    @abstractmethod
    def encode_token(self, username, password):
        raise NotImplementedError()

    @abstractmethod
    def get(self, record):
        raise NotImplementedError()

    @abstractmethod
    def create(self, prefix, record=None):
        raise NotImplementedError()

    @abstractmethod
    def update(self, record):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, record):
        raise NotImplementedError()


class ProviderManager(object):
    """Manage provider instances from a given provider name"""

    def __init__(self):
        self._provider_instances = {
            provider_name: None for provider_name in settings.ID_PROVIDER_SYSTEMS.keys()
        }

    def get(self, provider_name):
        if self._provider_instances[provider_name] is None:
            # Retrieve class name and module path
            id_provider_classpath = settings.ID_PROVIDER_SYSTEMS[provider_name][
                "class"
            ].split(".")
            id_provider_classname = id_provider_classpath[-1]
            id_provider_modpath = ".".join(id_provider_classpath[:-1])

            # Import module and class
            id_provider_module = import_module(id_provider_modpath)
            id_provider_class = getattr(id_provider_module, id_provider_classname)

            # Initialize handel system instance
            self._provider_instances[provider_name] = id_provider_class(
                provider_name, *settings.ID_PROVIDER_SYSTEMS[provider_name]["args"]
            )

        return self._provider_instances[provider_name]

    def find_provider_from_pid(self, pid):
        for provider_name in self._provider_instances.keys():
            provider = self.get(provider_name)

            if pid.startswith(provider.provider_url):
                return provider_name

        return None
