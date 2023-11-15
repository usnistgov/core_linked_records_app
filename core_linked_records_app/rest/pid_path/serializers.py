""" Serializers for calls related to `PidPath` model.
"""
from rest_framework import serializers

from core_linked_records_app.components.pid_path.models import PidPath


class PidPathSerializer(serializers.ModelSerializer):
    """Serializer for the `PidPath` model."""

    class Meta:
        """Meta"""

        model = PidPath
        fields = "__all__"
