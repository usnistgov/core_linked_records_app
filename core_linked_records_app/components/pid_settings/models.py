""" Linked Records Settings
"""
from django_mongoengine import Document
from mongoengine import errors as mongoengine_errors
from mongoengine import fields

from core_linked_records_app import settings
from core_main_app.commons import exceptions


class PidSettings(Document):
    auto_set_pid = fields.BooleanField(default=settings.AUTO_SET_PID)

    @staticmethod
    def get():
        try:
            return PidSettings.objects.first()
        except mongoengine_errors.DoesNotExist:
            return None
        except Exception as exc:
            raise exceptions.ModelError(str(exc))
