"""  Admin
"""

from django.contrib import admin

from core_linked_records_app.components.local_id.admin_site import CustomLocalIdAdmin
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.components.pid_xpath.admin_site import CustomPidXpathAdmin
from core_linked_records_app.components.pid_xpath.models import PidXpath

admin.site.register(LocalId, CustomLocalIdAdmin)
admin.site.register(PidSettings)
admin.site.register(PidXpath, CustomPidXpathAdmin)
