""" Linked records REST views
"""
import json
import logging
from importlib import import_module

from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app.settings import HANDLE_SYSTEMS

LOGGER = logging.getLogger("core_linked_records_app.rest.handle.views")


class HandleRecord(APIView):
    def __init__(self):
        self.handle_system_instances = {
            handle_system: None for handle_system in HANDLE_SYSTEMS.keys()
        }
        super().__init__()

    def _get_system_instance(self, system):
        if self.handle_system_instances[system] is None:
            # Retrieve class name and module path
            handle_system_classpath = HANDLE_SYSTEMS[system]["class"].split(".")
            handle_system_classname = handle_system_classpath[-1]
            handle_system_modpath = ".".join(handle_system_classpath[:-1])

            # Import module and class
            handle_system_module = import_module(handle_system_modpath)
            handle_system_class = getattr(
                handle_system_module, handle_system_classname
            )

            # Initialize handel system instance
            self.handle_system_instances[system] = handle_system_class(
                *HANDLE_SYSTEMS[system]["args"]
            )

        return self.handle_system_instances[system]

    def put(self, request, system, handle):
        """ Create a handle record

        Args:
            request:
            system:
            handle:

        Returns:
        """
        handle_system = self._get_system_instance(system)
        handle_response = handle_system.create(handle)

        handle_content = json.loads(handle_response.content)

        return Response(
            handle_content,
            status=handle_response.status_code
        )

    def post(self, request, system, handle):
        """ Update the value of a given handle record

        Args:
            request:
            system:
            handle:

        Returns:
        """
        handle_system = self._get_system_instance(system)
        handle_response = handle_system.update(handle)

        handle_content = json.loads(handle_response.content)

        return Response(
            handle_content,
            status=handle_response.status_code
        )

    def get(self, request, system, handle):
        """ Retrieve the local data of a given handle record

        Args:
            request:
            system:
            handle:

        Returns:
        """
        handle_system = self._get_system_instance(system)
        handle_response = handle_system.get(handle)

        handle_content = json.loads(handle_response.content)

        return Response(
            handle_content,
            status=handle_response.status_code
        )

    def delete(self, request, system, handle):
        """ Delete a handle record

        Args:
            request:
            system:
            handle:

        Returns:
        """
        handle_system = self._get_system_instance(system)
        handle_response = handle_system.delete(handle)

        handle_content = json.loads(handle_response.content)

        return Response(
            handle_content,
            status=handle_response.status_code
        )
