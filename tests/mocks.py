""" Mock classes for objects used within core_linked_records_app
"""
from unittest.mock import Mock

from rest_framework import status


class MockModule(Mock):
    """Mock Module"""

    def get_by_id(self, *args, **kwargs):
        """get_by_id

        Returns:
        """
        return "MockModule.get_by_id"


class MockLocalId(Mock):
    """Mock Local Id"""

    record_name = "mock_record_name"
    record_object_class = "mock.record.object.class"
    record_object_id = "mock_object_id"


class MockDocument(Mock):
    """Mock Document"""

    id = 1234
    pk = 1234


class MockData(MockDocument):
    """Mock Data"""

    dict_content = "mock_dict_content"


class MockPidSettings(Mock):
    """Mock Pid Settings"""

    auto_set_pid = True


class MockPidXpath(MockDocument):
    """Mock Pid Xpath"""

    xpath = "mock.xpath"
    template = 1234


class MockResponse(Mock):
    """Mock Response"""

    status_code = status.HTTP_200_OK
    data = dict()
    content = "{}"
    json_data = None

    def json(self):
        """json"""
        return self.json_data


class MockRequest(Mock):
    """Mock Request"""

    user = None


class MockProviderManager(Mock):
    """Mock Provider Manager"""

    provider_lookup_url = "mock_provider_url"
    create_exc = None
    create_result = None
    update_exc = None
    update_result = None
    get_exc = None
    get_result = None
    delete_exc = None
    delete_result = None

    def create(self, *args, **kwargs):
        """create"""
        if self.create_exc:
            raise self.create_exc

        return self.create_result

    def update(self, *args, **kwargs):
        """update"""
        if self.update_exc:
            raise self.update_exc

        return self.update_result

    def get(self, *args, **kwargs):
        """get"""
        if self.get_exc:
            raise self.get_exc

        return self.get_result

    def delete(self, *args, **kwargs):
        """delete"""
        if self.delete_exc:
            raise self.delete_exc

        return self.delete_result


class MockQuery(Mock):
    """Mock Query"""

    class MockTemplates(Mock):
        """Mock Templates"""

        templates = list()

        def all(self):
            """all"""
            return self.templates

    data_sources = list()
    content = ""
    templates = MockTemplates()


class MockDataSource(Mock):
    """Mock Data Source"""

    query_options = dict()
    order_by_field = ""
    capabilities = dict()


class MockAuthentication(Mock):
    """Mock Authentication"""

    type = ""


class MockSerializer(Mock):
    """Mock Serializer"""

    data = dict()
    is_valid_exc = None
    is_valid_result = True
    update_exc = None
    update_result = None

    def is_valid(self):
        """is_valid"""
        if self.is_valid_exc:
            raise self.is_valid_exc
        return self.is_valid_result

    def update(self, *args):
        """update"""
        if self.update_exc:
            raise self.update_exc
        return self.update_result


class MockInstance(Mock):
    """Mock Instance"""

    endpoint = "mock_endpoint"
    access_token = "mock_access_token"


class MockBlob(Mock):
    """Mock Blob"""

    blob = "mock_blob"
    filename = "mock_filename"
