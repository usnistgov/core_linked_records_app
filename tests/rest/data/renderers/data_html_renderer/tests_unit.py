"""Unit tests for data_html_renderer packages."""

from unittest import TestCase
from unittest.mock import patch, Mock

from rest_framework import status
from tests.mocks import MockRequest

from core_linked_records_app.rest.data.renderers.data_html_user_renderer import (
    DataHtmlUserRenderer,
)
from core_linked_records_app.rest.pid.views import DataHtmlRenderByPID
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)
from core_main_app.components.data.models import Data
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDataHtmlRenderByPID(TestCase):
    """TestDataHtmlRenderByPID"""

    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.render"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_api.get_by_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.acl_api.check_can_write"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_module_api.get_all_by_data_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.build_page"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.render_page"
    )
    def test_render_success(
        self,
        mock_render_page,
        mock_build_page,
        mock_get_data_modules,
        mock_check_can_write,
        mock_get_data,
        mock_render,
    ):
        # Arrange
        mock_request = MockRequest()
        mock_user = create_mock_user("1")
        mock_request.user = mock_user
        data = {"id": 1}
        renderer_context = {"request": mock_request, "kwargs": {}}
        mock_data = Mock(spec=Data)
        mock_get_data.return_value = mock_data
        mock_check_can_write.return_value = None
        mock_get_data_modules.return_value = []
        mock_build_page.return_value = {}
        mock_render_page.return_value = "<html>data</html>"

        # Act
        DataHtmlUserRenderer().render(data, renderer_context=renderer_context)

        # Assert
        self.assertTrue(mock_render.called)

    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.render"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_api.get_by_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.acl_api.check_can_write"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_module_api.get_all_by_data_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.build_page"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.render_page"
    )
    def test_render_cannot_edit_data(
        self,
        mock_render_page,
        mock_build_page,
        mock_get_data_modules,
        mock_check_can_write,
        mock_get_data,
        mock_render,
    ):
        # Arrange
        mock_request = MockRequest()
        mock_request.query_params = {}
        mock_user = create_mock_user("1")
        mock_request.user = mock_user
        data = {"id": 1}
        renderer_context = {"request": mock_request, "kwargs": {}}
        mock_data = Mock(spec=Data)
        mock_get_data.return_value = mock_data
        mock_check_can_write.side_effect = AccessControlError("forbidden")
        # Act
        DataHtmlUserRenderer().render(data, renderer_context=renderer_context)
        # Assert
        self.assertTrue(mock_build_page.called)

    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.render"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_api.get_by_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.acl_api.check_can_write"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_module_api.get_all_by_data_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.build_page"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.render_page"
    )
    def test_render_get_data_modules_success(
        self,
        mock_render_page,
        mock_build_page,
        mock_get_data_modules,
        mock_check_can_write,
        mock_get_data,
        mock_render,
    ):
        # Arrange
        mock_request = MockRequest()
        mock_request.query_params = {}
        mock_user = create_mock_user("1")
        mock_request.user = mock_user
        data = {"id": 1}
        renderer_context = {"request": mock_request, "kwargs": {}}
        mock_data = Mock(spec=Data)
        mock_get_data.return_value = mock_data
        mock_check_can_write.return_value = None
        mock_get_data_modules.return_value = ["module1", "module2"]
        mock_build_page.return_value = {}
        mock_render_page.return_value = "<html>data</html>"
        # Act
        DataHtmlUserRenderer().render(data, renderer_context=renderer_context)
        # Assert
        mock_get_data_modules.assert_called_once_with(
            data["id"],
            mock_request.user,
            run_strategy=AbstractProcessingModule.RUN_ON_DEMAND,
        )

    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.render"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_api.get_by_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.acl_api.check_can_write"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_module_api.get_all_by_data_id"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.build_page"
    )
    @patch(
        "core_linked_records_app.rest.data.renderers.data_html_user_renderer.data_view_builder.render_page"
    )
    def test_render_get_data_modules_access_control_error(
        self,
        mock_render_page,
        mock_build_page,
        mock_get_data_modules,
        mock_check_can_write,
        mock_get_data,
        mock_render,
    ):
        # Arrange
        mock_request = MockRequest()
        mock_request.query_params = {}
        mock_user = create_mock_user("1")
        mock_request.user = mock_user
        data = {"id": 1}
        renderer_context = {"request": mock_request, "kwargs": {}}
        mock_data = Mock(spec=Data)
        mock_get_data.return_value = mock_data
        mock_check_can_write.return_value = None
        mock_get_data_modules.side_effect = AccessControlError("forbidden")
        mock_build_page.return_value = {}
        mock_render_page.return_value = "<html>data</html>"
        # Act
        DataHtmlUserRenderer().render(data, renderer_context=renderer_context)
        # Assert
        mock_get_data_modules.assert_called_once_with(
            data["id"],
            mock_request.user,
            run_strategy=AbstractProcessingModule.RUN_ON_DEMAND,
        )

    def test_get_data_html_render_by_pid_returns_http_400_response_when_pid_is_missing(
        self,
    ):
        """test_get_data_html_render_by_pid_returns_http_400_response_when_pid_is_missing"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            DataHtmlRenderByPID.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
