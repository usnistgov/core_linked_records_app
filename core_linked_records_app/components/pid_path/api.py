"""API for PidPath model"""

import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_path.access_control import (
    can_get_by_template,
)
from core_linked_records_app.components.pid_path.models import PidPath
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.template import (
    api as template_api,
)

logger = logging.getLogger(__name__)


@access_control(can_get_by_template)
def get_by_template(template, user):  # noqa, pylint: disable=unused-argument
    """Retrieve PID paths associated with a specific template ID

    Args:
        template: Template
        user: User

    Returns:
        QuerySet - PidPath objects for the given template ID.
    """
    try:
        pid_paths = PidPath.get_by_template(template)

        # Returns a list containing a default PidPath if the template has none defined
        if not pid_paths.exists():
            return [
                PidPath(
                    template=template,
                    path=settings.PID_PATH,
                )
            ]

        return pid_paths
    except Exception as exc:
        error_message = (
            f"An unexpected error occurred while retrieving PidPaths "
            f"assigned to template {template.pk}"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(str(exc)) from exc


def get_all(request):
    """Retrieve all PID paths stored in `PidSettings`.

    Args:
        request (HttpRequest): The HTTP Request.

    Returns:
        list<str>: List of PID path.
    """
    try:
        return PidPath.get_all_by_template_list(
            [template.pk for template in template_api.get_all(request=request)]
        )
    except Exception as exc:
        error_message = (
            "An unexpected error occurred while retrieving all PidPath"
        )

        logger.error("%s: %s", error_message, str(exc))
        raise ApiError(str(exc)) from exc
