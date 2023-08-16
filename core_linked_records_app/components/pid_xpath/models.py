""" Linked records PID XPath objects.
"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_linked_records_app.utils.dict import validate_dot_notation
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template.models import Template

logger = logging.getLogger(__name__)


class PidXpath(models.Model):
    """Pid Xpath"""

    xpath = models.CharField(
        blank=False, max_length=255, validators=[validate_dot_notation]
    )
    template = models.OneToOneField(
        Template,
        blank=False,
        on_delete=models.CASCADE,
        null=False,
        unique=True,
    )

    @staticmethod
    def get_all():
        """Retrieve all PidXpath objects.

        Returns:
        """
        try:
            return PidXpath.objects.all()  # pylint: disable=no-member
        except Exception as exc:
            raise ModelError(str(exc)) from exc

    @staticmethod
    def get_all_by_template_list(template_list):
        """Retrieve a list of PidXpath given a list of templates.

        Args:
            template_list:

        Returns:
        """
        try:
            return PidXpath.objects.filter(  # pylint: disable=no-member
                template__in=template_list
            )
        except Exception as exc:
            raise ModelError(str(exc)) from exc

    @staticmethod
    def get_by_template(template):
        """Return all PidXpath defined for a given template.

        Args:
            template:

        Returns:
        """
        try:
            return PidXpath.objects.get(  # pylint: disable=no-member
                template=template
            )
        except ObjectDoesNotExist:
            return None
        except Exception as exc:
            raise exceptions.ModelError(str(exc)) from exc

    def __str__(self):
        """PidXpath object as string.

        Returns:
            str - String representation of PidXpath object.
        """
        return f"PID xpath '{self.xpath}' for template '{self.template}'"
