""" Linked records PID XPath objects.
"""
import logging
from django_mongoengine import Document
from mongoengine import errors as mongoengine_errors
from mongoengine import fields

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template.models import Template

logger = logging.getLogger(__name__)


class PidXpath(Document):
    xpath = fields.StringField(required=True)
    template = fields.ReferenceField(Template, required=True, unique=True)

    @staticmethod
    def get_all():
        try:
            return PidXpath.objects.all()
        except Exception as exc:
            raise ModelError(str(exc))

    @staticmethod
    def get_all_by_template_list(template_list):
        try:
            return PidXpath.objects.filter(template__in=template_list)
        except Exception as exc:
            raise ModelError(str(exc))

    @staticmethod
    def get_by_template_id(template_id):
        try:
            return PidXpath.objects.get(template=template_id)
        except mongoengine_errors.DoesNotExist:
            return None
        except Exception as exc:
            raise exceptions.ModelError(str(exc))
