""" Custom admin site for the Local Id model
"""
from django.contrib import admin


class CustomLocalIdAdmin(admin.ModelAdmin):
    """CustomLocalIdAdmin"""

    exclude = ["record_name", "record_object_class", "record_object_id"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Local ids"""
        return False
