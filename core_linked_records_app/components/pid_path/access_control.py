""" Access control helpers for PidPath APIs.
"""
from core_main_app.components.template.access_control import (
    check_can_read_template,
)


def can_get_by_template(func, template, user):
    """Check that user can use the `get_by_template` function.

    Args:
        func:
        template:
        user:

    Returns:
    """
    # Check can read template and PidPath
    check_can_read_template(template, user)
    return func(template, user)
