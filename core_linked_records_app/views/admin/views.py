""" Administration views
"""
from urllib.parse import urljoin

from django.urls import reverse
from django.views.generic import View

from core_linked_records_app.settings import SERVER_URI
from core_main_app.components.template import api as template_api
from core_main_app.utils.rendering import admin_render
from core_main_app.utils.requests_utils.requests_utils import send_get_request


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

        settings_rest_url = reverse("core_linked_records_app_settings")
        settings_response = send_get_request(
            urljoin(SERVER_URI, settings_rest_url),
            cookies={
                "sessionid": request.session.session_key,
            },
        )

        if settings_response.status_code != 200:
            return admin_render(
                request,
                "core_linked_records_app/admin/pid_settings_error.html",
                context={
                    "error": "An error occured while retrieving the PID settings. "
                    "Please contact an administrator for more information."
                },
            )

        pid_xpath_rest_url = reverse(
            "core_linked_records_app_settings_xpath_list"
        )
        xpath_response = send_get_request(
            urljoin(SERVER_URI, pid_xpath_rest_url),
            cookies={
                "sessionid": request.session.session_key,
            },
        )

        if xpath_response.status_code != 200:
            return admin_render(
                request,
                "core_linked_records_app/admin/pid_settings_error.html",
                context={
                    "error": "An error occured while retrieving the list of PID XPath. "
                    "Please contact an administrator for more information."
                },
            )

        xpath_settings = {}

        # Retrieve existing PidXpath
        for xpath_item in xpath_response.json():
            xpath_template = template_api.get_by_id(
                xpath_item["template"], request
            )
            xpath_settings[xpath_template.display_name] = {
                "xpath": xpath_item["xpath"],
                "edit_url": reverse(
                    "admin:core_linked_records_app_pidxpath_change",
                    args=(xpath_item["id"],),
                ),
            }

        response_dict = settings_response.json()
        response_dict["xpath"] = {"default": {"xpath": response_dict["xpath"]}}
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
