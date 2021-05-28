""" Serializers for calls related to `PidSettings` model.
"""
from rest_framework_mongoengine import serializers

from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.components.pid_settings import api as pid_settings_api


class PidSettingsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PidSettings

    def update(self, instance: PidSettings, validated_data):
        """Update a PidSetting instance

        Args:
            instance:
            validated_data:

        Returns:
            Updated PidSettings instance
        """
        instance.auto_set_pid = validated_data["auto_set_pid"]
        return pid_settings_api.upsert(instance)
