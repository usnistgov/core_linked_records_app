""" Serializer classes for LocalID object
"""
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_linked_records_app.components.local_id.models import LocalId


class LocalIdSerializer(DocumentSerializer):
    """LocalId serializer"""

    class Meta(object):
        model = LocalId
        fields = "__all__"
        read_only_fields = ["record_name", "record_object_class", "record_object_id"]
