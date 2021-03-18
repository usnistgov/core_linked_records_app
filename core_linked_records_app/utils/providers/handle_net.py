""" Handle.net implementation class
"""
import json
import logging
from base64 import b64encode

from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.utils.requests_utils.requests_utils import (
    send_put_request,
    send_delete_request,
    send_get_request,
)

LOGGER = logging.getLogger(__name__)


class HandleNetSystem(AbstractIdProvider):
    """Provider implemented using Handle.Net."""

    registration_api = "api/handles"
    response_code_messages = {
        1: "Successful operation",
        2: "Unexpected handle server error",
        100: "Handle not found",
        101: "Handle already exists",
        102: "Invalid handle",
        200: "Values not found",
        201: "Value already exists",
        202: "Invalid value",
        301: "Server not responsible for handle",
        402: "Authentication needed",
    }

    def _get_message_for_response_code(self, return_code):
        if return_code in self.response_code_messages.keys():
            return self.response_code_messages[return_code]
        else:
            return "Handle code not recognized"

    def _update_response_content(self, response):
        json_response_content = json.loads(response.content)

        json_response_content["message"] = self._get_message_for_response_code(
            json_response_content["responseCode"]
        )

        json_response_content["url"] = "%s/%s" % (
            self.provider_url,
            json_response_content["handle"],
        )

        return json.dumps(json_response_content)

    def encode_token(self, username, password):
        user_pass = "%s:%s" % (username, password)
        return b64encode(user_pass.encode("utf-8")).decode("utf-8")

    def get(self, record):
        """Retrieve an existring handle.net handle.

        Args:
            record:

        Returns:
        """
        response = send_get_request(
            "%s/%s/%s" % (self.provider_url, self.registration_api, record),
            headers={
                "Content-Type": "application/json",
            },
        )

        response._content = self._update_response_content(response)
        return response

    def create(self, prefix, record=None):
        """Create a new handle for a handle.net system.

        Args:
            prefix:
            record:

        Returns:
        """
        # Create request url depending on handle value
        if record is not None:
            request_url = "%s/%s/%s/%s?overwrite=false" % (
                self.provider_url,
                self.registration_api,
                prefix,
                record,
            )
        else:
            request_url = "%s/%s/%s/?overwrite=false&mintNewSuffix=true" % (
                self.provider_url,
                self.registration_api,
                prefix,
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
                                "value": "%s/%s/%s" % (self.local_url, prefix, record),
                            },
                        }
                    ]
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic %s" % str(self.auth_token),
            },
        )

        if record is None:
            return self.update(response.json()["handle"])
        else:
            response._content = self._update_response_content(response)
            return response

    def update(self, record):
        """Update a handle for a handle.net system.

        Args:
            record:

        Returns:
        """
        response = send_put_request(
            "%s/%s/%s?overwrite=true"
            % (self.provider_url, self.registration_api, record),
            json.dumps(
                {
                    "handle": record,
                    "values": [
                        {
                            "index": 100,
                            "type": "URL",
                            "data": {
                                "format": "string",
                                "value": "%s/%s" % (self.local_url, record),
                            },
                        }
                    ],
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic %s" % str(self.auth_token),
            },
        )

        response._content = self._update_response_content(response)
        return response

    def delete(self, record):
        response = send_delete_request(
            "%s/%s/%s" % (self.provider_url, self.registration_api, record),
            headers={"Authorization": "Basic %s" % str(self.auth_token)},
        )

        response._content = self._update_response_content(response)
        return response
