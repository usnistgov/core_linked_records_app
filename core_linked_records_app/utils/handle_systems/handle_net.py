""" Handle.net implementation class
"""
import json
import logging

from base64 import b64encode

from django.urls import reverse

from core_linked_records_app.utils.handle_systems import AbstractHandleSystem
from core_main_app.utils.requests_utils.requests_utils import \
    send_put_request, send_delete_request, send_get_request

LOGGER = logging.getLogger(
    "core_linked_records_app.utils.handle_systems.handle_net"
)


class HandleNetSystem(AbstractHandleSystem):
    """
    """
    handle_code_messages = {
        1: "Successful operation",
        2: "Unexpected handle server error",
        100: "Handle not found",
        101: "Handle already exists",
        102: "Invalid handle",
        200: "Values not found",
        201: "Value already exists",
        202: "Invalid value",
        301: "Server not responsible for handle",
        402: "Authentication needed"
    }

    def _get_message_for_handle_code(self, handle_code):
        if handle_code in self.handle_code_messages.keys():
            return self.handle_code_messages[handle_code]
        else:
            return "Handle code not recognized"

    def _update_response_content(self, response):
        json_response_content = json.loads(response.content)

        json_response_content["message"] = self._get_message_for_handle_code(
            json_response_content["responseCode"]
        )

        json_response_content["url"] = "%s/%s" % (
            self.handle_url,
            json_response_content["handle"]
        )

        return json.dumps(json_response_content)

    def encode_token(self, username, password):
        user_pass = "%s:%s" % (username, password)
        return b64encode(user_pass.encode("utf-8")).decode("utf-8")

    def get(self, handle):
        """ Create a new handle for a handle.net system.

        Args:
            handle:

        Returns:
        """
        response = send_get_request(
            "%s/%s" % (self.handle_url, handle),
            headers={
                "Content-Type": "application/json",
            }
        )

        response._content = self._update_response_content(response)
        return response

    def create(self, prefix, handle=None):
        """ Create a new handle for a handle.net system.

        Args:
            prefix:
            handle:

        Returns:
        """
        # Create request url depending on handle value
        if handle is not None:
            request_url = "%s/%s/%s?overwrite=false" % (
                self.handle_url, prefix, handle
            )
        else:
            request_url = "%s/%s/?overwrite=false&mintNewSuffix=true" % (
                self.handle_url, prefix
            )

        response = send_put_request(
            request_url,
            json.dumps(
                {
                    "values": [
                        {
                            "index": 100,
                            "type": "URL",
                            "data": {
                                "format": "string",
                                "value": "%s%s" % (
                                    self.local_url,
                                    reverse(
                                        "core_linked_records_app_rest_handle_record_view",
                                        kwargs={
                                            "system": "handle.net",
                                            "handle": handle
                                        }
                                    )
                                )
                            }
                        }
                    ]
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic %s" % str(self.auth_token)
            }
        )

        response._content = self._update_response_content(response)
        return response

    def update(self, handle):
        """ Update a handle for a handle.net system.

        Args:
            handle:

        Returns:
        """
        response = send_put_request(
            "%s/%s?overwrite=true" % (self.handle_url, handle),
            json.dumps(
                {
                    "handle": handle,
                    "values": [
                        {
                            "index": 100,
                            "type": "URL",
                            "data": {
                                "format": "string",
                                "value": "%s%s" % (
                                    self.local_url,
                                    reverse(
                                        "core_linked_records_app_rest_handle_record_view",
                                        kwargs={
                                            "system": "handle.net",
                                            "handle": handle
                                        }
                                    )
                                )
                            }
                        }
                    ]
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic %s" % str(self.auth_token)
            }
        )

        response._content = self._update_response_content(response)
        return response

    def delete(self, handle):
        response = send_delete_request(
            "%s/%s" % (self.handle_url, handle),
            headers={
                "Authorization": "Basic %s" % str(self.auth_token)
            }
        )

        response._content = self._update_response_content(response)
        return response
