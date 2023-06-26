""" Administration views
"""

from django.urls import reverse
from django.views.generic import View

from core_linked_records_app.components.pid_xpath import api as pid_xpath_api
from core_linked_records_app.settings import SERVER_URI
from core_linked_records_app.utils.pid import get_pid_settings_dict
from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
)
from core_main_app.utils.rendering import admin_render


class PidSettingsView(View):
    """View to display PID settings in the admin part"""

    def get(self, request):
        """HTTP GET method"""
        context = {}

        assets = {
            "js": [
                {
                    "path": "core_linked_records_app/admin/js/pid_settings/auto_set_pid.js",
                    "is_raw": True,
                }
            ],
            "css": [
                "core_linked_records_app/admin/css/pid_settings.css",
            ],
        }

        xpath_settings = {}

        # Retrieve existing PidXpath
        try:
            for xpath_item in pid_xpath_api.get_all(request):
                xpath_settings[xpath_item.template.display_name] = {
                    "xpath": xpath_item.xpath,
                    "edit_url": reverse(
                        "admin:core_linked_records_app_pidxpath_change",
                        args=(xpath_item.pk,),
                    ),
                }

            pid_settings = pid_settings_api.get()
            response_dict = get_pid_settings_dict(pid_settings)
            response_dict["xpath"] = {
                "default": {"xpath": response_dict["xpath"]}
            }
            response_dict["xpath"].update(xpath_settings)

            response_dict["add_xpath_url"] = reverse(
                "admin:core_linked_records_app_pidxpath_add"
            )

            record_sample_url = reverse(
                "core_linked_records_provider_record",
                kwargs={
                    "provider": response_dict["system_name"],
                    "record": f"{response_dict['prefixes'][0]}/record",
                },
            )
            response_dict["sample_url"] = f"{SERVER_URI}{record_sample_url}"

            context.update({"pid_settings": response_dict})

            return admin_render(
                request,
                "core_linked_records_app/admin/pid_settings.html",
                assets=assets,
                context=context,
            )
        except Exception as exc:
            return admin_render(
                request,
                "core_linked_records_app/admin/pid_settings_error.html",
                context={
                    "error": "An error occured while retrieving the PID settings. "
                    "Please contact an administrator for more information. Exception: "
                    f"{str(exc)}."
                },
            )
