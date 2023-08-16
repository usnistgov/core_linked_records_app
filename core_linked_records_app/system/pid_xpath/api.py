""" System API to manage PidXpath objects.
"""
import logging

from core_linked_records_app import settings
from core_linked_records_app.components.pid_xpath.models import PidXpath

logger = logging.getLogger(__name__)


def get_pid_xpath_by_template(template):
    """Retrieve XPath associated with a specific template ID

    Args:
        template: Template object

    Returns:
        PidXpath - PidXpath object, linking template ID and XPath
    """
    pid_xpath_object = PidXpath.get_by_template(template)

    if pid_xpath_object is None:
        return PidXpath(template=template, xpath=settings.PID_XPATH)

    return pid_xpath_object
