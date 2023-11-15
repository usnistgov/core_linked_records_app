""" Administration views
"""

from django.urls import reverse
from django.views.generic import View

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
)
from core_linked_records_app.components.pid_path import api as pid_path_api
from core_linked_records_app.settings import SERVER_URI
from core_linked_records_app.utils.pid import get_pid_settings_dict
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
                    "is_raw": False,
                }
            ],
            "css": [
                "core_linked_records_app/admin/css/pid_settings.css",
            ],
        }

        pid_path_settings = {}

        # Retrieve existing PidPath
        try:
            for pid_path_item in pid_path_api.get_all(request):
                pid_path_settings[pid_path_item.template.display_name] = {
                    "path": pid_path_item.path,
                    "edit_url": reverse(
                        "admin:core_linked_records_app_pidpath_change",
                        args=(pid_path_item.pk,),
                    ),
                }

            pid_settings = pid_settings_api.get(request.user)
            response_dict = get_pid_settings_dict(pid_settings)
            response_dict["path"] = {
                "default": {"path": response_dict["path"]}
            }
            response_dict["path"].update(pid_path_settings)

            response_dict["add_path_url"] = reverse(
                "admin:core_linked_records_app_pidpath_add"
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
