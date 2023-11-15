"""  Admin
"""

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_linked_records_app.components.local_id.admin_site import (
    CustomLocalIdAdmin,
)
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.components.pid_settings.admin_site import (
    CustomPidSettingsAdmin,
)
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.components.pid_path.admin_site import (
    CustomPidPathAdmin,
)
from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.views.admin import views as admin_views
from core_main_app.admin import core_admin_site

admin_urls = [
    re_path(
        r"^pid/settings/$",
        staff_member_required(admin_views.PidSettingsView.as_view()),
        name="core_linked_records_app_admin_settings",
    ),
]

admin.site.register(LocalId, CustomLocalIdAdmin)
admin.site.register(PidSettings, CustomPidSettingsAdmin)
admin.site.register(PidPath, CustomPidPathAdmin)

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
