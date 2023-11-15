""" System API to manage PidPath objects.
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_path.models import PidPath

logger = logging.getLogger(__name__)


def get_pid_path_by_template(template):
    """Retrieve path associated with a specific template ID

    Args:
        template: Template object

    Returns:
        PidPath - PidPath object, linking template ID and path
    """
    pid_path_object = PidPath.get_by_template(template)

    if pid_path_object is None:
        return PidPath(template=template, path=settings.PID_PATH)

    return pid_path_object
