""" Linked Records Settings
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class PidSettings(models.Model):
    """Pid Settings"""

    auto_set_pid = models.BooleanField(default=False)

    @staticmethod
    def get():
        """Retrieve the PidSettings.

        Returns:
             PidSettings - first PidSettings object
        """
        try:
            return PidSettings.objects.first()
        except ObjectDoesNotExist:
            return None
        except Exception as exc:
            raise exceptions.ModelError(str(exc))

    def __str__(self):
        """LocalId object as string.

        Returns:
            str - String representation of PidSettings object.
        """
        return f"PidSettings {{ id:{self.pk}; auto_set_pid:{self.auto_set_pid} }}"
