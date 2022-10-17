""" Unit tests for menus
"""
from unittest import TestCase

from menu import Menu

from core_linked_records_app.menus import pid_settings_menu, admin_menu


class TestMenus(TestCase):
    """Test menus module"""

    def test_pid_settings_menu_in_admin_menu(self):
        """test_pid_settings_menu_in_admin_menu"""
        self.assertIn(pid_settings_menu, admin_menu.children)

    def test_admin_menu_in_loaded_menus(self):
        """test_admin_menu_in_loaded_menus"""
        Menu.load_menus()
        self.assertIn(admin_menu, Menu.items["admin"])
