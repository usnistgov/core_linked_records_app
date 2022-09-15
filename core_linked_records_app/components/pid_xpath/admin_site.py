""" Custom admin site for the Pid Xpath model
"""
from django.contrib import admin


class CustomPidXpathAdmin(admin.ModelAdmin):
    """CustomPidXpathAdmin"""

    exclude = ["_cls", "url"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Pid Xpaths"""
        return False
