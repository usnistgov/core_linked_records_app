""" Local handle model
"""
from django_mongoengine import fields, Document
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES

from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class LocalId(Document):
    """ Handle object
    """
    record_name = fields.StringField(
        blank=False,
        unique=True,
        regex=NOT_EMPTY_OR_WHITESPACES
    )

    @staticmethod
    def get_by_name(record_name):
        try:
            return LocalId.objects.get(record_name=record_name)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
