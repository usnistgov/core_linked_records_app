""" Serializers for calls related to `PidXpath` model.
"""
from rest_framework import serializers

from core_linked_records_app.components.pid_xpath.models import PidXpath


class PidXpathSerializer(serializers.ModelSerializer):
    """Pid Xpath Serializer"""

    class Meta:
        """Meta"""

        model = PidXpath
        fields = "__all__"
