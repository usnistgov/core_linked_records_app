""" Custom admin site for the PidSettings model
"""
from django.contrib import admin


class CustomPidSettingsAdmin(admin.ModelAdmin):
    """CustomPidSettingsAdmin"""

    def has_add_permission(
        self, request, obj=None
    ):  # pylint: disable=unused-argument
        """Prevent from manually adding PidSettings"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent from manually deleting PidSettings"""
        return False
