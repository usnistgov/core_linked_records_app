""" Local record system implementation
"""
import json
import random
import string

from django.urls import reverse
from requests import Response
from rest_framework import status

from core_linked_records_app.components.local_id import api as record_api
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import NotUniqueError


class LocalIdProvider(AbstractIdProvider):
    def __init__(self, base_url):
        api_url = "%s%s" % (
            base_url,
            reverse(
                "core_linked_records_app_rest_provider_record_view",
                kwargs={
                    "provider": "local",
                    "record": "@record@"
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

    def is_id_already_used(self, record):
        return json.loads(
            self.get(record).content
        )["message"] == "Successful operation"

    def get(self, record):
        response = Response()
        response_url = self.provider_url.replace("@record@", record)

        try:
            record_api.get_by_name(record)
            response.status_code = status.HTTP_200_OK
            response._content = json.dumps(
                {
                    "message": "Successful operation",
                    "record": record,
                    "url": response_url
                }
            )
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps(
                {
                    "message": "record not found",
                    "record": record,
                    "url": response_url
                }
            )

        return response

    def create(self, prefix, record=None):
        if record is None:
            # FIXME: duplicate code with core_main_registry_app
            # Create new record randomly
            record = self._generate_id()

            # While the record exists, retry creation of record
            while self.is_id_already_used("%s/%s" % (prefix, record)):
                record = self._generate_id()

        record = "%s/%s" % (prefix, record)

        response = Response()
        response_content = {
            "record": record,
            "url": self.provider_url.replace("@record@", record)
        }

        try:
            record_object = LocalId(
                record_name=record
            )

            record_api.insert(record_object)

            response.status_code = status.HTTP_201_CREATED
            response_content["message"] = "Successful operation"
        except NotUniqueError:
            response.status_code = status.HTTP_409_CONFLICT
            response_content["message"] = "record already exists"

        response._content = json.dumps(response_content)
        return response

    def update(self, record):
        self.create(record)

        response = Response()
        response._content = json.dumps({
            "record": record,
            "message": "Successful operation",
            "url": self.provider_url.replace("@record@", record)
        })

        return response

    def delete(self, record):
        response = Response()

        try:
            record_object = record_api.get_by_name(record)
            record_object.delete()

            response._content = json.dumps({
                "record": record,
                "message": "Successful operation",
                "url": self.provider_url.replace("@record@", record)
            })
        except exceptions.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            response._content = json.dumps({
                "record": record,
                "message": "record not found",
                "url": self.provider_url.replace("@record@", record)
            })

        return response
