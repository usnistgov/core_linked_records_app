""" Unit tests for data_xml_renderer packages.
"""
from unittest import TestCase

from core_linked_records_app.rest.data.renderers.data_xml_renderer import (
    DataXmlRenderer,
)


class TestDataXmlRendererRender(TestCase):
    """Unit tests for `DataXmlRenderer.render` method."""

    def test_xml_renderer_returns_data_content(self):
        """test_xml_renderer_returns_data_content"""
        data_content = "<root></root>"
        mock_data = {"xml_content": data_content}
        renderer = DataXmlRenderer()
        result = renderer.render(mock_data)
        self.assertEqual(result, data_content)
