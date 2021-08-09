""" Unit tests for core_linked_records_app.system.api
"""
from unittest import TestCase


class TestIsPidDefinedForDocument(TestCase):
    def test_wrong_document_id_raise_error(self):
        pass

    def test_undefined_pid_returns_false(self):
        pass

    def test_duplicate_pid_returns_false(self):
        pass

    def test_defined_pid_for_other_document_returns_false(self):
        pass

    def test_defined_pid_for_current_document_returns_true(self):
        pass


class TestIsPidDefined(TestCase):
    def test_get_data_by_pid_fails_with_unexpected_error_raises_error(self):
        pass

    def test_get_data_by_pid_fails_with_expected_error_returns_false(self):
        pass

    def test_get_data_by_pid_succeeds_return_true(self):
        pass


class TestGetDataByPid(TestCase):
    def test_query_returns_no_results_raises_error(self):
        pass

    def test_query_returns_several_results_raises_error(self):
        pass

    def test_query_returns_single_result_returns_result(self):
        pass


class TestGetPidForData(TestCase):
    def test_not_existing_pid_returns_none(self):
        pass

    def test_existing_pid_returns_pid(self):
        pass
