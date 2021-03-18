""" Local handle model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class LocalId(Document):
    """Handle object"""

    record_name = fields.StringField(
        blank=False, unique=True, regex=NOT_EMPTY_OR_WHITESPACES
    )
    record_object_class = fields.StringField(blank=True)
    record_object_id = fields.StringField(blank=True)

    @staticmethod
    def get_by_name(record_name):
        try:
            return LocalId.objects.get(record_name=record_name)
        except mongoengine_errors.DoesNotExist as dne:
            raise exceptions.DoesNotExist(str(dne))
        except Exception as exc:
            raise exceptions.ModelError(str(exc))

    @staticmethod
    def get_by_class_and_id(record_object_class, record_object_id):
        try:
            return LocalId.objects.get(
                record_object_class=record_object_class,
                record_object_id=record_object_id,
            )
        except mongoengine_errors.DoesNotExist as dne:
            raise exceptions.DoesNotExist(str(dne))
        except Exception as exc:
            raise exceptions.ModelError(str(exc))
