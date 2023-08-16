""" Local handle model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class LocalId(models.Model):
    """Handle object"""

    record_name = models.CharField(
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=255,
    )
    record_object_class = models.CharField(blank=True, max_length=255)
    record_object_id = models.CharField(blank=True, max_length=255)

    @staticmethod
    def get_by_name(record_name):
        """Retrieve LocalId object with the given record_name.

        Args:
            record_name:

        Returns:
            LocalId - LocalId object if found.
        """
        try:
            return LocalId.objects.get(  # pylint: disable=no-member
                record_name=record_name
            )
        except ObjectDoesNotExist as dne:
            raise exceptions.DoesNotExist(str(dne))
        except Exception as exc:
            raise exceptions.ModelError(str(exc))

    @staticmethod
    def get_by_class_and_id(record_object_class, record_object_id):
        """Retrieve LocalId object given record_object_class and record_object_id.

        Args:
            record_object_class:
            record_object_id:

        Returns:
            LocalId - LocalId object if found.
        """
        try:
            return LocalId.objects.get(  # pylint: disable=no-member
                record_object_class=record_object_class,
                record_object_id=record_object_id,
            )
        except ObjectDoesNotExist as dne:
            raise exceptions.DoesNotExist(str(dne))
        except Exception as exc:
            raise exceptions.ModelError(str(exc))

    @staticmethod
    def upsert(local_id_object):
        """Insert a new LocalId object

        Args:
            local_id_object:

        Returns:
        """
        try:
            local_id_object.save()
            return local_id_object
        except IntegrityError as nue:
            raise exceptions.NotUniqueError(str(nue))
        except Exception as exc:
            raise exceptions.ModelError(str(exc))

    def __str__(self):
        """LocalId object as string.

        Returns:
            str - String representation of LocalId object.
        """
        return f"LocalId {self.record_name}"
