""" API for PidXpath model
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import (
    api as template_api,
)

logger = logging.getLogger(__name__)


def get_by_template_id(template_id, request):
    """Retrieve XPath associated with a specific template ID

    Args:
        template_id: ObjectId
        request: HttpRequest

    Returns:
        str - XPath for the given template ID
    """
    try:
        if template_id not in [
            template.pk for template in template_api.get_all(request=request)
        ]:
            raise AccessControlError("Template not accessible to the current user")

        pid_xpath_object = PidXpath.get_by_template_id(template_id)

        if pid_xpath_object is None:
            return PidXpath(template=template_id, xpath=settings.PID_XPATH)
        else:
            return pid_xpath_object
    except AccessControlError as ace:
        raise AccessControlError(str(ace))
    except Exception as exc:
        error_message = (
            f"An unexpected error occurred while retrieving PidXpath "
            f"assigned to template {template_id}"
        )

        logger.error(f"{error_message}: {str(exc)}")
        raise ApiError(str(exc))


def get_all(request):
    """Retrieve all XPath stored in `PidSettings`

    Args:
        request: HttpRequest

    Returns:
        list<str> - List of XPath
    """
    try:
        return PidXpath.get_all_by_template_list(
            [template.pk for template in template_api.get_all(request=request)]
        )
    except Exception as exc:
        error_message = f"An unexpected error occurred while retrieving all PidXpath"

        logger.error(f"{error_message}: {str(exc)}")
        raise ApiError(str(exc))
