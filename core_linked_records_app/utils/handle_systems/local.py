""" Local handle system implementation
"""
import json
import random
import string

from django.urls import reverse
from requests import Response
from rest_framework import status

from core_linked_records_app.components.handle import api as handle_api
from core_linked_records_app.components.handle.models import Handle
from core_linked_records_app.utils.handle_systems import AbstractHandleSystem
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import NotUniqueError


class LocalHandleSystem(AbstractHandleSystem):
    def __init__(self, base_url):
        api_url = "%s%s" % (
            base_url,
            reverse(
                "core_linked_records_app_rest_handle_record_view",
                kwargs={
                    "system": "local",
                    "handle": "@handle@"
                }
            )
        )

        super().__init__(api_url, base_url, None, None)

    def encode_token(self, username, password):
        return None

    @staticmethod
    def _generate_id(length_id=16):
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length_id)
        )

    def is_id_already_used(self, handle):
        return json.loads(
            self.get(handle).content
        )["message"] == "Successful operation"

    def get(self, handle):
        response = Response()
        response_url = self.handle_url.replace("@handle@", handle)

        try:
            handle_api.get_by_name(handle)
            response.status_code = status.HTTP_200_OK
            response._content = json.dumps(
                {
                    "message": "Successful operation",
                    "handle": handle,
                    "url": response_url
                }
            )
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps(
                {
                    "message": "Handle not found",
                    "handle": handle,
                    "url": response_url
                }
            )

        return response

    def create(self, prefix, handle=None):
        if handle is None:
            # FIXME: duplicate code with core_main_registry_app
            # Create new handle randomly
            handle = "%s/%s" % (prefix, self._generate_id())

            # While the handle exists, retry creation of handle
            while self.is_id_already_used(handle):
                handle = "%s/%s" % (prefix, self._generate_id())

        response = Response()
        response_content = {
            "handle": handle,
            "url": self.handle_url.replace("@handle@", handle)
        }

        try:
            handle_object = Handle(
                handle_name=handle
            )

            handle_api.insert(handle_object)

            response.status_code = status.HTTP_201_CREATED
            response_content["message"] = "Successful operation"
        except NotUniqueError:
            response.status_code = status.HTTP_409_CONFLICT
            response_content["message"] = "Handle already exists"

        response._content = json.dumps(response_content)
        return response

    def update(self, handle):
        self.create(handle)

        response = Response()
        response._content = json.dumps({
            "handle": handle,
            "message": "Successful operation",
            "url": self.handle_url.replace("@handle@", handle)
        })

        return response

    def delete(self, handle):
        response = Response()

        try:
            handle_object = handle_api.get_by_name(handle)
            handle_object.delete()

            response._content = json.dumps({
                "handle": handle,
                "message": "Successful operation",
                "url": self.handle_url.replace("@handle@", handle)
            })
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps({
                "handle": handle,
                "message": "Handle not found",
                "url": self.handle_url.replace("@handle@", handle)
            })

        return response


