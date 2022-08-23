""" Serializer classes for LocalID object
"""
from rest_framework.serializers import ModelSerializer

from core_linked_records_app.components.local_id.models import LocalId


class LocalIdSerializer(ModelSerializer):
    """LocalId serializer"""

    class Meta:
        """Meta"""

        model = LocalId
        fields = "__all__"
        read_only_fields = ["record_name", "record_object_class", "record_object_id"]
