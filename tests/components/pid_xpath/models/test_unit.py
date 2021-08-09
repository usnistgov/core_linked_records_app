""" Unit tests for core_linked_records_app.components.pid_xpath.models
"""
from unittest import TestCase

from mongoengine import errors as mongoengine_errors
from unittest.mock import patch

from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_main_app.commons.exceptions import ModelError


class TestPidXpathGetAll(TestCase):
    @patch.object(PidXpath, "objects")
    def test_pid_xpath_all_failure_raises_model_error(self, mock_pid_xpath):
        mock_pid_xpath.all.side_effect = Exception("mock_pid_xpath_all_exception")

        with self.assertRaises(ModelError):
            PidXpath.get_all()

    @patch.object(PidXpath, "objects")
    def test_returns_pid_xpath_all_output(self, mock_pid_xpath):
        expected_result = "mock_pid_xpath_all"
        mock_pid_xpath.all.return_value = expected_result

        self.assertEquals(PidXpath.get_all(), expected_result)


class TestPidXpathGetByTemplateList(TestCase):
    @patch.object(PidXpath, "objects")
    def test_pid_xpath_filter_failure_raises_model_error(self, mock_pid_xpath):
        mock_pid_xpath.filter.side_effect = Exception("mock_pid_xpath_filter_exception")

        with self.assertRaises(ModelError):
            PidXpath.get_all_by_template_list("mock_template_list")

    @patch.object(PidXpath, "objects")
    def test_returns_pid_xpath_filter_output(self, mock_pid_xpath):
        expected_result = "mock_pid_xpath_filter"
        mock_pid_xpath.filter.return_value = expected_result

        self.assertEquals(
            PidXpath.get_all_by_template_list("mock_template_list"), expected_result
        )


class TestPidXpathGetByTemplateId(TestCase):
    @patch.object(PidXpath, "objects")
    def test_pid_xpath_get_does_not_exists_returns_none(self, mock_pid_xpath):
        mock_pid_xpath.get.side_effect = mongoengine_errors.DoesNotExist()

        self.assertIsNone(PidXpath.get_by_template_id("mock_template_id"))

    @patch.object(PidXpath, "objects")
    def test_pid_xpath_get_raises_model_error(self, mock_pid_xpath):
        mock_pid_xpath.get.side_effect = Exception("mock_pid_xpath_get_exception")

        with self.assertRaises(ModelError):
            PidXpath.get_by_template_id("mock_template_id")

    @patch.object(PidXpath, "objects")
    def test_returns_pid_xpath_get_output(self, mock_pid_xpath):
        expected_result = "mock_pid_xpath_get"
        mock_pid_xpath.get.return_value = expected_result

        self.assertEquals(
            PidXpath.get_by_template_id("mock_template_id"), expected_result
        )
