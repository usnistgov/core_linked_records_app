""" Local record system implementation
"""
import json
import random
import string

from requests import Response
from rest_framework import status

from core_main_app.commons import exceptions
from core_linked_records_app.components.local_id import api as record_api
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.utils.providers import AbstractIdProvider


class LocalIdProvider(AbstractIdProvider):
    """Local Id Provider"""

    def __init__(self, provider_name):
        super().__init__(provider_name, None, None, None, None)

    def encode_token(self, username, password):
        return None

    @staticmethod
    def _generate_id(length_id=16):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length_id)
        )

    def is_id_already_used(self, record):
        """is_id_already_used
        Args:
            record

        Returns:
        """
        return json.loads(self.get(record).content)["message"] == "Successful operation"

    def get(self, record):
        """get

        Args:
            record:

        Returns:
        """

        response = Response()

        record_url = "%s/%s" % (self.provider_lookup_url, record)

        try:
            record_api.get_by_name(record)
            response.status_code = status.HTTP_200_OK
            response._content = json.dumps(
                {
                    "message": "Successful operation",
                    "record": record,
                    "url": record_url,
                }
            )
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps(
                {"message": "record not found", "record": record, "url": record_url}
            )

        return response

    def create(self, prefix, record=None):
        """create

        Args:
            prefix:
            record:

        Returns:
        """

        if record is None:
            # FIXME: duplicate code with core_main_registry_app
            # Create new record randomly
            record = self._generate_id()

            # While the record exists, retry creation of record
            while self.is_id_already_used(f"{prefix}/{record}"):
                record = self._generate_id()

        record = f"{prefix}/{record}"
        record_url = f"{self.provider_lookup_url}/{record}"

        response = Response()
        response_content = {
            "record": record,
            "url": record_url,
        }

        try:
            record_object = LocalId(record_name=record)

            record_api.insert(record_object)

            response.status_code = status.HTTP_201_CREATED
            response_content["message"] = "Successful operation"
        except exceptions.NotUniqueError:
            response.status_code = status.HTTP_409_CONFLICT
            response_content["message"] = "record already exists"

        response._content = json.dumps(response_content)
        return response

    def update(self, record):
        """update

        Args:
            record:

        Returns:
        """
        self.create(record)

        record_url = f"{self.provider_lookup_url}/{record}"

        response = Response()
        response._content = json.dumps(
            {
                "record": record,
                "message": "Successful operation",
                "url": record_url,
            }
        )

        return response

    def delete(self, record):
        """delete

        Args:
            record:

        Returns:
        """
        response = Response()

        record_url = f"{self.provider_lookup_url}/{record}"

        try:
            record_object = record_api.get_by_name(record)
            record_object.delete()

            response._content = json.dumps(
                {
                    "record": record,
                    "message": "Successful operation",
                    "url": record_url,
                }
            )
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps(
                {
                    "record": record,
                    "message": "record not found",
                    "url": record_url,
                }
            )

        return response
