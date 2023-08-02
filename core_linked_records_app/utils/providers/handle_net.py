""" Handle.net implementation class
"""
import json
import logging
from base64 import b64encode

from core_linked_records_app import settings
from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.utils.requests_utils.requests_utils import (
    send_put_request,
    send_delete_request,
    send_get_request,
)

logger = logging.getLogger(__name__)


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

    def __init__(
        self,
        provider_name,
        provider_lookup_url,
        provider_registration_url,
        username,
        password,
    ):
        self.provider_registration_url = provider_registration_url
        self.auth_token = b64encode(
            f"{username}:{password}".encode("utf-8")
        ).decode("utf-8")
        super().__init__(provider_name, provider_lookup_url)

    def _get_message_for_response_code(self, return_code):
        if return_code in self.response_code_messages.keys():
            return self.response_code_messages[return_code]

        return "Handle code not recognized"

    def _update_response_content(self, response):
        json_response_content = json.loads(response.content)

        json_response_content["message"] = self._get_message_for_response_code(
            json_response_content["responseCode"]
        )

        json_response_content[
            "url"
        ] = f'{self.provider_lookup_url}/{ json_response_content["handle"]}'

        return json.dumps(json_response_content)

    def _generate_record_data(self, record, include_handle=False):
        record_data = {
            "values": [
                {
                    "index": settings.HANDLE_NET_RECORD_INDEX,
                    "type": "URL",
                    "data": {
                        "format": "string",
                        "value": f"{self.local_url}/{record}",
                    },
                },
                settings.HANDLE_NET_ADMIN_DATA,
            ]
        }

        if include_handle:
            record_data["handle"] = record

        return json.dumps(record_data)

    def get(self, record):
        """Retrieve an existring handle.net handle.

        Args:
            record:

        Returns:
        """
        response = send_get_request(
            f"{self.provider_lookup_url}/{self.registration_api}/{record}",
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
            request_url = f"{self.provider_registration_url}/{self.registration_api}/{prefix}/{record}?overwrite=false"

        else:
            request_url = f"{self.provider_registration_url}/{self.registration_api}/{prefix}/?overwrite=false&mintNewSuffix=true"

        response = send_put_request(
            request_url,
            self._generate_record_data(f"{prefix}/{record}"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {str(self.auth_token)}",
            },
        )

        if record is None:
            return self.update(response.json()["handle"])

        response._content = self._update_response_content(response)
        return response

    def update(self, record):
        """Update a handle for a handle.net system.

        Args:
            record:

        Returns:
        """
        response = send_put_request(
            f"{self.provider_registration_url}/{self.registration_api}/"
            f"{record}?overwrite=true",
            self._generate_record_data(record, include_handle=True),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {str(self.auth_token)}",
            },
        )

        response._content = self._update_response_content(response)
        return response

    def delete(self, record):
        response = send_delete_request(
            f"{self.provider_registration_url}/{self.registration_api}/{record}",
            headers={"Authorization": f"Basic {str(self.auth_token)}"},
        )

        response._content = self._update_response_content(response)
        return response
