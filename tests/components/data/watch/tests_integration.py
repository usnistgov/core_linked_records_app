""" Integration tests for data watchers (creation / deletion of PIDs when data are
created / deleted).
"""
from os.path import join

from core_linked_records_app.settings import (
    ID_PROVIDER_PREFIX_DEFAULT,
    ID_PROVIDER_SYSTEM_NAME,
)
from core_linked_records_app.utils import (
    exceptions as linked_records_exceptions,
)
from core_main_app.commons import exceptions as main_exceptions
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.fixtures import DataFixtures
from tests.test_settings import SERVER_URI


class TestRecordCreationWithDuplicatePid(IntegrationTransactionTestCase):
    """Integration tests checking the creation of two data with duplicate PID."""

    fixture = DataFixtures()

    def setUp(self):  # pylint: disable=invalid-name
        """setUp"""
        self.user = create_mock_user(1)
        self.mock_pid = "pid1"
        self.mock_pid_url = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid,
        )
        super().setUp()

    def test_create_duplicate_pid_is_not_possible_when_pid_enabled(
        self,
    ):
        """test_create_duplicate_pid_is_not_possible_when_pid_enabled"""
        # Arrange: Enable PID.
        self.fixture.auto_set_pid(True)

        # Act: Load data 1 with PID 1.
        self.fixture.insert_record("record_1", self.mock_pid_url, self.user)

        # Assert: Ensure creating data 2 with PID 1 raises an exception.
        with self.assertRaises(
            main_exceptions.ModelError,
            msg="PID already defined for another instance",
        ):
            self.fixture.insert_record(
                "record_2", self.mock_pid_url, self.user
            )

    def test_create_duplicate_pid_is_possible_when_pid_disabled(self):
        """test_create_duplicate_pid_is_possible_when_pid_disabled"""
        # Arrange: Disable PID
        self.fixture.auto_set_pid(False)

        # Act / Assert: Load data 1 with PID 1 then data 2 with PID 1. No exception
        #   should occur.
        self.fixture.insert_record("record_1", self.mock_pid_url, self.user)
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)

    def test_create_duplicate_pid_is_not_possible_after_pid_enabled(
        self,
    ):
        """test_create_duplicate_pid_is_not_possible_after_pid_enabled"""
        # Arrange: Disable PID.
        self.fixture.auto_set_pid(False)

        # Act: Load data 1 with PID 1 then enable PIDs.
        self.fixture.insert_record("record_1", self.mock_pid_url, self.user)
        self.fixture.auto_set_pid(True)

        # Assert: Ensure creating data 2 with PID 1 raises an exception.
        with self.assertRaises(
            main_exceptions.ModelError,
            msg="PID already defined for another instance",
        ):
            self.fixture.insert_record(
                "record_2", self.mock_pid_url, self.user
            )

    def test_create_duplicate_pid_is_possible_after_pid_disabled(
        self,
    ):
        """test_create_duplicate_pid_is_possible_after_pid_disabled"""
        # Arrange: Enable PID.
        self.fixture.auto_set_pid(True)

        # Act / Assert: Load data 1 with PID 1, disable PIDs and, create data 2 with
        #   PID 1. No exception should occur.
        self.fixture.insert_record("record_1", self.mock_pid_url, self.user)
        self.fixture.auto_set_pid(False)
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)


class TestRecordCreationWithDeletedPid(IntegrationTransactionTestCase):
    """Integration tests checking the creation of a data containing a deleted
    PID."""

    fixture = DataFixtures()

    def setUp(self):  # pylint: disable=invalid-name
        """setUp"""
        self.user = create_mock_user(1)
        self.mock_pid = "pid1"
        self.mock_pid_url = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid,
        )
        super().setUp()

    def test_create_record_is_possible_when_pid_enabled(self):
        """test_create_record_is_possible_when_pid_enabled"""
        self.fixture.auto_set_pid(True)

        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url, self.user
        )
        data_1.delete()

        # Act / Assert: Creating record should not raise any exception.
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)

    def test_create_record_pid_is_possible_when_pid_disabled(self):
        """test_create_record_pid_is_possible_when_pid_disabled"""
        # Arrange: Disable PID + create & delete record.
        self.fixture.auto_set_pid(False)

        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url, self.user
        )
        data_1.delete()

        # Act / Assert: Creating record should not raise any exception.
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)

    def test_create_record_pid_is_possible_after_pid_enabled(
        self,
    ):
        """test_create_record_pid_is_possible_after_pid_enabled"""
        # Arrange: Disable PID + create & delete data.
        self.fixture.auto_set_pid(False)

        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url, self.user
        )
        data_1.delete()

        # Act / Assert: Enable PID + check creating a new record with the same PID does
        #   not raise any exception.
        self.fixture.auto_set_pid(True)
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)

    def test_create_record_pid_is_possible_after_pid_disabled(
        self,
    ):
        """test_create_record_pid_is_possible_after_pid_disabled"""
        # Arrange: Enable PID + create & delete record.
        self.fixture.auto_set_pid(True)

        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url, self.user
        )
        data_1.delete()

        # Act / Assert: Disable PID + check creating a new record with the same PID does
        #   not raise any exception.
        self.fixture.auto_set_pid(False)
        self.fixture.insert_record("record_2", self.mock_pid_url, self.user)


class TestRecordModificationToNewPid(IntegrationTransactionTestCase):
    """Integration tests checking the modification of a data, changing the existing PID
    to a new, unregistered, PID.
    """

    fixture = DataFixtures()

    def setUp(self):  # pylint: disable=invalid-name
        """setUp"""
        self.user = create_mock_user(1)
        self.mock_pid_1 = "pid1"
        self.mock_pid_url_1 = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid_1,
        )
        self.mock_pid_2 = "pid2"
        self.mock_pid_url_2 = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid_2,
        )
        super().setUp()

    def test_modify_record_is_possible_when_pid_enabled(
        self,
    ):
        """test_modify_record_is_possible_when_pid_enabled"""
        # Arrange: Enable PID + create record_1 with PID 1.
        self.fixture.auto_set_pid(True)
        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url_1, self.user
        )

        # Act / Assert: Modify record_1 to PID 2 should not raise any exception.
        data_1.xml_content = data_1.xml_content.replace(
            self.mock_pid_url_1, self.mock_pid_url_2
        )
        data_1.save()

    def test_modify_record_pid_is_possible_when_pid_disabled(self):
        """test_modify_record_pid_is_possible_when_pid_disabled"""
        # Arrange: Disable PID + create record_1 with PID 1.
        self.fixture.auto_set_pid(False)
        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url_1, self.user
        )

        # Act / Assert: Modify record_1 to PID 2 should not raise any exception.
        data_1.xml_content = data_1.xml_content.replace(
            self.mock_pid_url_1, self.mock_pid_url_2
        )
        data_1.save()

    def test_modify_record_pid_is_possible_after_pid_enabled(
        self,
    ):
        """test_modify_record_pid_is_possible_after_pid_enabled"""
        # Arrange: Disable PID + create record_1 with PID 1.
        self.fixture.auto_set_pid(False)
        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url_1, self.user
        )

        # Act / Assert: Enable PID & check that modifying record_1 to PID 2 does not
        #   raise any exception.
        self.fixture.auto_set_pid(True)
        data_1.xml_content = data_1.xml_content.replace(
            self.mock_pid_url_1, self.mock_pid_url_2
        )
        data_1.save()

    def test_modify_record_pid_is_possible_after_pid_disabled(
        self,
    ):
        """test_modify_record_pid_is_possible_after_pid_disabled"""
        # Arrange: Enable PID + create record_1 with PID 1.
        self.fixture.auto_set_pid(True)
        data_1 = self.fixture.insert_record(
            "record_1", self.mock_pid_url_1, self.user
        )

        # Act / Assert: Disable PID & check that modifying record_1 to PID 2 does not
        #   raise any exception.
        self.fixture.auto_set_pid(False)
        data_1.xml_content = data_1.xml_content.replace(
            self.mock_pid_url_1, self.mock_pid_url_2
        )
        data_1.save()


class TestRecordModificationToExistingPid(IntegrationTransactionTestCase):
    """Integration tests checking the modification of a data, changing the existing PID
    to an already registered PID.
    """

    fixture = DataFixtures()

    def setUp(self):  # pylint: disable=invalid-name
        """setUp"""
        self.user = create_mock_user(1)
        self.mock_pid_1 = "pid1"
        self.mock_pid_url_1 = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid_1,
        )
        self.mock_pid_2 = "pid2"
        self.mock_pid_url_2 = join(
            SERVER_URI,
            "rest",
            ID_PROVIDER_SYSTEM_NAME,
            ID_PROVIDER_PREFIX_DEFAULT,
            self.mock_pid_2,
        )
        super().setUp()

    def test_modify_record_is_not_possible_when_pid_enabled(
        self,
    ):
        """test_modify_record_is_not_possible_when_pid_enabled"""
        # Arrange: Enable PID + create record_1 with PID 1 and record_2 with PID 2.
        self.fixture.auto_set_pid(True)
        self.fixture.insert_record("record_1", self.mock_pid_url_1, self.user)
        data_2 = self.fixture.insert_record(
            "record_2", self.mock_pid_url_2, self.user
        )

        # Act: Change data_2 pid to PID 1.
        data_2.xml_content = data_2.xml_content.replace(
            self.mock_pid_url_2, self.mock_pid_url_1
        )

        # Assert: Saving the data should raise an error.
        with self.assertRaises(
            linked_records_exceptions.PidCreateError,
            msg="PID already defined for another instance",
        ):
            data_2.save()

    def test_modify_record_pid_is_possible_when_pid_disabled(self):
        """test_modify_record_pid_is_possible_when_pid_disabled"""
        # Arrange: Disalbe PID + create record_1 with PID 1 and record_2 with PID 2
        self.fixture.auto_set_pid(False)
        self.fixture.insert_record("record_1", self.mock_pid_url_1, self.user)
        data_2 = self.fixture.insert_record(
            "record_2", self.mock_pid_url_2, self.user
        )

        # Act: Change data_2 pid to PID 1.
        data_2.xml_content = data_2.xml_content.replace(
            self.mock_pid_url_2, self.mock_pid_url_1
        )

        # Assert: Saving the data should not raise an error.
        data_2.save()

    def test_modify_record_pid_is_not_possible_after_pid_enabled(
        self,
    ):
        """test_modify_record_pid_is_not_possible_after_pid_enabled"""
        # Arrange: Disable PID + create record_1 with PID 1 and record_2 with PID 2
        self.fixture.auto_set_pid(False)
        self.fixture.insert_record("record_1", self.mock_pid_url_1, self.user)
        data_2 = self.fixture.insert_record(
            "record_2", self.mock_pid_url_2, self.user
        )

        # Act: Enable PID + Change data_2 pid to PID 1
        self.fixture.auto_set_pid(True)
        data_2.xml_content = data_2.xml_content.replace(
            self.mock_pid_url_2, self.mock_pid_url_1
        )

        # Assert: Saving the data should raise an error.
        with self.assertRaises(
            linked_records_exceptions.PidCreateError,
            msg="PID already defined for another instance",
        ):
            data_2.save()

    def test_modify_record_pid_is_possible_after_pid_disabled(
        self,
    ):
        """test_modify_record_pid_is_possible_after_pid_disabled"""
        # Arrange: Enable PID + create record_1 with PID 1 and record_2 with PID 2
        self.fixture.auto_set_pid(True)
        self.fixture.insert_record("record_1", self.mock_pid_url_1, self.user)
        data_2 = self.fixture.insert_record(
            "record_2", self.mock_pid_url_2, self.user
        )

        # Act: Disable PID + Change data_2 pid to PID 1
        self.fixture.auto_set_pid(False)
        data_2.xml_content = data_2.xml_content.replace(
            self.mock_pid_url_2, self.mock_pid_url_1
        )

        # Assert: Saving the data should not raise an error.
        data_2.save()
