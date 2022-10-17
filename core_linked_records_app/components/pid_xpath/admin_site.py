""" Custom admin site for the Pid Xpath model
"""
from django.contrib import admin


class CustomPidXpathAdmin(admin.ModelAdmin):
    """CustomPidXpathAdmin"""

    exclude = ["_cls", "url"]
