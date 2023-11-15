""" Custom admin site for the `PidPath` model.
"""
from django.contrib import admin


class CustomPidPathAdmin(admin.ModelAdmin):
    """CustomPidPathAdmin model"""

    exclude = ["_cls", "url"]
