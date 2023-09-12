""" Serializers for calls related to `PidSettings` model.
"""
from rest_framework import serializers

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
)
from core_linked_records_app.components.pid_settings.models import (
    PidSettings,
)


class PidSettingsSerializer(serializers.ModelSerializer):
    """Pid Settings Serializer"""

    class Meta:
        """Meta"""

        model = PidSettings
        exclude = ["id"]

    def update(self, instance: PidSettings, validated_data):
        """Update a PidSetting instance

        Args:
            instance:
            validated_data:

        Returns:
            Updated PidSettings instance
        """
        instance.auto_set_pid = validated_data["auto_set_pid"]
        return pid_settings_api.upsert(instance, self.context["request"].user)
