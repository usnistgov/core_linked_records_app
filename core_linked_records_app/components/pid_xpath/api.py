""" API for PidXpath model
"""
from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template import (
    api as template_api,
)


def get_by_template_id(template_id, request):
    """Retrieve XPath associated with a specific template ID

    Args:
        template_id: ObjectId
        request: HttpRequest

    Returns:
        str - XPath for the given template ID
    """
    if template_id not in [
        template.pk for template in template_api.get_all(request=request)
    ]:
        raise AccessControlError("Template not accessible to the current user")

    pid_xpath_object = PidXpath.get_by_template_id(template_id)

    if pid_xpath_object is None:
        return PidXpath(template=template_id, xpath=settings.PID_XPATH)
    else:
        return pid_xpath_object


def get_all(request):
    """Retrieve all XPath stored in `PidSettings`

    Args:
        request: HttpRequest

    Returns:
        list<str> - List of XPath
    """
    return PidXpath.get_all_by_template_list(
        [template.pk for template in template_api.get_all(request=request)]
    )
