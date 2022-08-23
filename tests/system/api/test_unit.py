""" Unit tests for core_linked_records_app.system.api
"""
from unittest import TestCase


class TestIsPidDefinedForDocument(TestCase):
    """Test Is Pid Defined For Document"""

    def test_wrong_document_id_raise_error(self):
        """test_wrong_document_id_raise_error"""

        pass

    def test_undefined_pid_returns_false(self):
        """test_undefined_pid_returns_false"""

        pass

    def test_duplicate_pid_returns_false(self):
        """test_duplicate_pid_returns_false"""

        pass

    def test_defined_pid_for_other_document_returns_false(self):
        """test_defined_pid_for_other_document_returns_false"""

        pass

    def test_defined_pid_for_current_document_returns_true(self):
        """test_defined_pid_for_current_document_returns_true"""

        pass


class TestIsPidDefined(TestCase):
    """Test Is Pid Defined"""

    def test_get_data_by_pid_fails_with_unexpected_error_raises_error(self):
        """test_get_data_by_pid_fails_with_unexpected_error_raises_error"""

        pass

    def test_get_data_by_pid_fails_with_expected_error_returns_false(self):
        """test_get_data_by_pid_fails_with_expected_error_returns_false"""

        pass

    def test_get_data_by_pid_succeeds_return_true(self):
        """test_get_data_by_pid_succeeds_return_true"""

        pass


class TestGetDataByPid(TestCase):
    """Test Get Data By Pid"""

    def test_query_returns_no_results_raises_error(self):
        """test_query_returns_no_results_raises_error"""

        pass

    def test_query_returns_several_results_raises_error(self):
        """test_query_returns_several_results_raises_error"""

        pass

    def test_query_returns_single_result_returns_result(self):
        """test_query_returns_single_result_returns_result"""

        pass


class TestGetPidForData(TestCase):
    """Test Get Pid For Data"""

    def test_not_existing_pid_returns_none(self):
        """test_not_existing_pid_returns_none"""

        pass

    def test_existing_pid_returns_pid(self):
        """test_existing_pid_returns_pid"""

        pass
