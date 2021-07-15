""" Serializers for calls related to `PidXpath` model.
"""
from rest_framework_mongoengine import serializers

from core_linked_records_app.components.pid_xpath.models import PidXpath


class PidXpathSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PidXpath
