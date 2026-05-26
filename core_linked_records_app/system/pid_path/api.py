"""System API to manage PidPath objects."""

import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_path.models import PidPath

logger = logging.getLogger(__name__)


def get_pid_path_by_template(template):
    """Retrieve path associated with a specific template ID.

    For multi-path templates, returns the first path (backwards compatibility).
    Callers that need to handle multiple paths should use get_all_pid_paths_by_template.

    Args:
        template: Template object

    Returns:
        PidPath - PidPath object, linking template ID and path
    """
    pid_path_queryset = PidPath.get_by_template(template)

    if not pid_path_queryset.exists():
        return PidPath(template=template, path=settings.PID_PATH)

    return pid_path_queryset.first()


def get_all_pid_paths_by_template(template):
    """Retrieve all paths associated with a specific template ID.

    Always returns a list so callers can rely on len() and indexing.

    Args:
        template: Template object

    Returns:
        list[PidPath] - All PidPath objects for the template, or [default] if none exist
    """
    pid_path_queryset = PidPath.get_by_template(template)

    if not pid_path_queryset.exists():
        return [PidPath(template=template, path=settings.PID_PATH)]

    return list(pid_path_queryset)
