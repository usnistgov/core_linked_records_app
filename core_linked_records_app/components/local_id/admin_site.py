""" Custom admin site for the LocalId model
"""
from django.contrib import admin


class CustomLocalIdAdmin(admin.ModelAdmin):
    """CustomLocalIdAdmin"""

    def has_add_permission(
        self, request, obj=None
    ):  # pylint: disable=unused-argument
        """Prevent from manually adding LocalID objects"""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent from manually editing LocalID objects"""
        return False
