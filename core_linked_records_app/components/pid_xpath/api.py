""" API for PidXpath model
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.access_control import (
    can_get_by_template,
)
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import (
    api as template_api,
)

logger = logging.getLogger(__name__)


@access_control(can_get_by_template)
def get_by_template(template, user):  # noqa, pylint: disable=unused-argument
    """Retrieve XPath associated with a specific template ID

    Args:
        template: Template
        user: User

    Returns:
        str - XPath for the given template ID
    """
    try:
        pid_xpath_object = PidXpath.get_by_template(template)

        # Returns default PID_XPATH settings if the template has no defined PidXpath
        if pid_xpath_object is None:
            return PidXpath(
                template=template,
                xpath=settings.PID_XPATH,
            )

        return pid_xpath_object
    except Exception as exc:
        error_message = (
            f"An unexpected error occurred while retrieving PidXpath "
            f"assigned to template {template.pk}"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(str(exc)) from exc


def get_all(request):
    """Retrieve all XPath stored in `PidSettings`.

    Args:
        request (HttpRequest): The HTTP Request.

    Returns:
        list<str>: List of XPath.
    """
    try:
        return PidXpath.get_all_by_template_list(
            [template.pk for template in template_api.get_all(request=request)]
        )
    except Exception as exc:
        error_message = (
            "An unexpected error occurred while retrieving all PidXpath"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(str(exc)) from exc
