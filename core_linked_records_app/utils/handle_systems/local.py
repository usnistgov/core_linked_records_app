""" Local handle system implementation
"""
import json

from requests import Response

from core_main_app.commons import exceptions
from core_linked_records_app.components.handle.models import Handle
from core_linked_records_app.components.handle import api as handle_api
from core_linked_records_app.utils.handle_systems import AbstractHandleSystem
from core_main_app.commons.exceptions import NotUniqueError


class LocalHandleSystem(AbstractHandleSystem):
    def __init__(self, base_url):
        super().__init__(base_url, None, None, None)

    def encode_token(self, username, password):
        return None

    def get(self, handle):
        response = Response()

        try:
            handle_api.get_by_name(handle)
            response._content = json.dumps(
                {
                    "message": "Successful operation",
                    "handle": handle
                }
            )
        except exceptions.DoesNotExist:
            response._content = json.dumps(
                {
                    "message": "Handle not found",
                    "handle": handle
                }
            )

        return response

    def create(self, handle):
        response = Response()
        response_content = {
            "handle": handle
        }

        try:
            handle_object = Handle(
                handle_name=handle
            )

            handle_api.insert(handle_object)

            response_content["message"] = "Successful operation"
        except NotUniqueError:
            response_content["message"] = "Handle already exists"

        response._content = json.dumps(response_content)
        return response

    def update(self, handle):
        self.create(handle)

        response = Response()
        response._content = json.dumps({
            "handle": handle,
            "message": "Successful operation"
        })

        return response

    def delete(self, handle):
        response = Response()

        try:
            handle_object = handle_api.get_by_name(handle)
            handle_object.delete()

            response._content = json.dumps({
                "handle": handle,
                "message": "Successful operation"
            })
        except exceptions.DoesNotExist:
            response._content = json.dumps({
                "handle": handle,
                "message": "Handle not found"
            })

        return response


