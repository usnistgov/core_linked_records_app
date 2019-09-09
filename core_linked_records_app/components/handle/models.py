""" Local handle model
"""
from django_mongoengine import fields, Document
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES

from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class Handle(Document):
    """ Handle object
    """
    handle_name = fields.StringField(
        blank=False,
        unique=True,
        regex=NOT_EMPTY_OR_WHITESPACES
    )

    @staticmethod
    def get_by_name(handle_name):
        try:
            return Handle.objects.get(handle_name=handle_name)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
