""" Mock classes for objects used within core_linked_records_app
"""
from bson import ObjectId
from rest_framework import status
from unittest.mock import Mock


class MockModule(Mock):
    def get_by_id(self, *args, **kwargs):
        return "MockModule.get_by_id"


class MockLocalId(Mock):
    record_name = "mock_record_name"
    record_object_class = "mock.record.object.class"
    record_object_id = "mock_object_id"


class MockDocument(Mock):
    id = ObjectId()
    pk = ObjectId()


class MockData(MockDocument):
    dict_content = "mock_dict_content"


class MockPidSettings(Mock):
    auto_set_pid = True


class MockPidXpath(MockDocument):
    xpath = "mock.xpath"
    template = ObjectId()


class MockResponse(Mock):
    status_code = status.HTTP_200_OK
    data = dict()
    content = "{}"
    json_data = None

    def json(self):
        return self.json_data


class MockRequest(Mock):
    user = None


class MockProviderManager(Mock):
    provider_url = "mock_provider_url"
    create_exc = None
    create_result = None
    update_exc = None
    update_result = None
    get_exc = None
    get_result = None
    delete_exc = None
    delete_result = None

    def create(self, *args, **kwargs):
        if self.create_exc:
            raise self.create_exc

        return self.create_result

    def update(self, *args, **kwargs):
        if self.update_exc:
            raise self.update_exc

        return self.update_result

    def get(self, *args, **kwargs):
        if self.get_exc:
            raise self.get_exc

        return self.get_result

    def delete(self, *args, **kwargs):
        if self.delete_exc:
            raise self.delete_exc

        return self.delete_result


class MockQuery(Mock):
    data_sources = list()
    content = ""
    templates = list()


class MockDataSource(Mock):
    query_options = dict()
    order_by_field = ""
    capabilities = dict()


class MockAuthentication(Mock):
    type = ""


class MockSerializer(Mock):
    data = dict()
    is_valid_exc = None
    is_valid_result = True
    update_exc = None
    update_result = None

    def is_valid(self):
        if self.is_valid_exc:
            raise self.is_valid_exc
        return self.is_valid_result

    def update(self, *args):
        if self.update_exc:
            raise self.update_exc
        return self.update_result


class MockInstance(Mock):
    endpoint = "mock_endpoint"
    access_token = "mock_access_token"


class MockBlob(Mock):
    blob = "mock_blob"
    filename = "mock_filename"
