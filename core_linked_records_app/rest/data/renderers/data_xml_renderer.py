""" Data Xml renderer for django REST API
"""
from rest_framework import renderers


class DataXmlRenderer(renderers.BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """ Render the data object by just returning the xml_content field

        Args:
            data:
            media_type:
            renderer_context:

        Returns: xml string
        """
        return data['xml_content']
