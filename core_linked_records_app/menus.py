""" Menu configuration for core_linked_records_app.
Upon installation of the app the following menus are displayed:

  * Admin menu

    * PID settings
"""
from django.urls import reverse
from menu import Menu, MenuItem

pid_settings_menu = MenuItem(
    "PID Settings",
    reverse("core-admin:core_linked_records_app_admin_settings"),
    icon="cogs",
)

admin_menu = MenuItem("LINKED RECORDS", None, children=(pid_settings_menu,))

Menu.add_item("admin", admin_menu)
