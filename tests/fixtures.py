"""Fixtures for data integration tests cases."""

from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.system import api as system_api
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class DataFixtures(FixtureInterface):
    """Data fixtures."""

    pid_settings: PidSettings = None
    template = None

    def insert_data(self):
        """Automatically inserts data."""
        self.create_pid_settings()
        self.insert_template()

    def create_pid_settings(self):
        """Creates PID settings"""
        self.pid_settings = PidSettings()
        pid_settings_system_api.upsert(self.pid_settings)

    def auto_set_pid(self, auto_set_pid_value: bool):
        """Change the value of the auto_set_pid field, enabling or disabling PID."""
        self.pid_settings.auto_set_pid = auto_set_pid_value
        pid_settings_system_api.upsert(self.pid_settings)

    def insert_record(self, data_name, data_pid, user):
        """Insert a record given a name, PID and user"""
        xml_content = (
            f"<mock><pid>{data_pid}</pid><name>{data_name}</name></mock>"
        )

        data = Data(
            template=self.template,
            user_id=user.id,
            title=data_name,
            xml_content=xml_content,
        )
        system_api.upsert_data(data)
        return data

    def insert_template(self):
        """Generate a unique Template."""
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="mock">'
            "<xs:complexType>"
            "<xs:sequence>"
            '<xs:element name="pid"></xs:element>'
            '<xs:element name="name"></xs:element>'
            "</xs:sequence>"
            "</xs:complexType>"
            "</xs:element>"
            "</xs:schema>"
        )
        self.template.content = xsd
        self.template.format = "XSD"
        self.template.hash = ""
        self.template.filename = "filename"
        self.template.save()


class MultiPIDsDataFixtures(FixtureInterface):
    """MultiPIDs Data fixtures."""

    pid_settings: PidSettings = None
    xml_template = None
    json_template = None
    pid_path_1 = None
    pid_path_2 = None

    def insert_data(self):
        """Automatically inserts data."""
        self.create_pid_settings()
        self.insert_templates()

    def create_pid_settings(self):
        """Creates PID settings"""
        self.pid_settings = PidSettings()
        pid_settings_system_api.upsert(self.pid_settings)

    def auto_set_pid(self, auto_set_pid_value: bool):
        """Change the value of the auto_set_pid field, enabling or disabling PID."""
        self.pid_settings.auto_set_pid = auto_set_pid_value
        pid_settings_system_api.upsert(self.pid_settings)

    def insert_pid_paths(self, template, path_1=None, path_2=None):
        if path_1:
            self.pid_path_1 = PidPath(path=path_1, template=template)
            self.pid_path_1.save()
        if path_2:
            self.pid_path_2 = PidPath(path=path_2, template=template)
            self.pid_path_2.save()

    def insert_record(self, content, data_name, user, template):
        data = Data(
            template=template,
            user_id=user.id,
            title=data_name,
            xml_content=content,
        )
        system_api.upsert_data(data)
        return data

    def insert_templates(self):
        """Generate XML and JSON Templates."""
        # Insert XML template
        self.xml_template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="mock">'
            "<xs:complexType>"
            "<xs:sequence>"
            '<xs:element name="pid1" minOccurs="0"></xs:element>'
            '<xs:element name="pid2" minOccurs="0"></xs:element>'
            "</xs:sequence>"
            "</xs:complexType>"
            "</xs:element>"
            "</xs:schema>"
        )
        self.xml_template.content = xsd
        self.xml_template.format = "XSD"
        self.xml_template.hash = ""
        self.xml_template.filename = "filename.xsd"
        self.xml_template.save()

        # Insert JSON template
        self.json_template = Template()
        json_schema = "{}"
        self.json_template.format = "JSON"
        self.json_template.content = json_schema
        self.json_template.hash = ""
        self.json_template.filename = "filename.json"
        self.json_template.save()
