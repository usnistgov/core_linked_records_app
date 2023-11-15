""" Mock classes for objects used within core_linked_records_app
"""
from unittest.mock import Mock

from rest_framework import status


class MockModule(Mock):
    """Mock Module"""

    get_by_id_return_value = "MockModule.get_by_id"

    def get_by_id(
        self, *args, **kwargs  # noqa, pylint: disable=unused-argument
    ):
        """get_by_id

        Returns:
        """
        return self.get_by_id_return_value


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


class MockTemplate(Mock):
    """Mock Template"""

    display_name = None


class MockPidSettings(Mock):
    """Mock Pid Settings"""

    auto_set_pid = True


class MockPidPath(MockDocument):
    """Mock PidPath object"""

    path = "mock.path"
    template = 1234


class MockResponse(Mock):
    """Mock Response"""

    status_code = status.HTTP_200_OK
    data = {}
    content = "{}"
    json_data = None

    def json(self):
        """json"""
        return self.json_data


class MockSession(Mock):
    """MockSession"""

    session_key = "mock_session"


class MockRequest(Mock):
    """Mock Request"""

    user = None
    session = MockSession()


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

    def create(self, *args, **kwargs):  # noqa, pylint: disable=unused-argument
        """create"""
        if self.create_exc and issubclass(self.create_exc, Exception):
            raise self.create_exc  # pylint: disable=raising-bad-type

        return self.create_result

    def update(self, *args, **kwargs):  # noqa, pylint: disable=unused-argument
        """update"""
        if self.update_exc and issubclass(self.update_exc, Exception):
            raise self.update_exc  # pylint: disable=raising-bad-type

        return self.update_result

    def get(self, *args, **kwargs):  # noqa, pylint: disable=unused-argument
        """get"""
        if self.get_exc and issubclass(self.get_exc, Exception):
            raise self.get_exc  # pylint: disable=raising-bad-type

        return self.get_result

    def delete(self, *args, **kwargs):  # noqa, pylint: disable=unused-argument
        """delete"""
        if self.delete_exc and issubclass(self.delete_exc, Exception):
            raise self.delete_exc  # pylint: disable=raising-bad-type

        return self.delete_result


class MockQuery(Mock):
    """Mock Query"""

    class MockTemplates(Mock):
        """Mock Templates"""

        templates = []

        def all(self):
            """all"""
            return self.templates

    data_sources = []
    content = ""
    templates = MockTemplates()


class MockDataSource(Mock):
    """Mock Data Source"""

    query_options = {}
    order_by_field = ""
    capabilities = {}


class MockAuthentication(Mock):
    """Mock Authentication"""

    auth_type = ""


class MockSerializer(Mock):
    """Mock Serializer"""

    data = {}
    is_valid_exc = None
    is_valid_result = True
    update_exc = None
    update_result = None

    def is_valid(self):
        """is_valid"""
        if self.is_valid_exc and issubclass(self.is_valid_exc, Exception):
            raise self.is_valid_exc  # pylint: disable=raising-bad-type
        return self.is_valid_result

    def update(self, *args):  # noqa, pylint: disable=unused-argument
        """update"""
        if self.update_exc and issubclass(self.update_result, Exception):
            raise self.update_exc  # pylint: disable=raising-bad-type
        return self.update_result


class MockInstance(Mock):
    """Mock Instance"""

    endpoint = "mock_endpoint"
    access_token = "mock_access_token"


class MockBlob(Mock):
    """Mock Blob"""

    blob = Mock()
    filename = "mock_filename"
