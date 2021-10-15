""" REST views for PidXPath collection
"""
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.rest.pid_xpath.serializers import PidXpathSerializer


class PidXpathListView(ListCreateAPIView):
    """View for listing and creating `PidXPath` objects"""

    permission_classes = (IsAuthenticated,)

    queryset = PidXpath.objects.all()
    serializer_class = PidXpathSerializer


class PidXpathDetailView(RetrieveUpdateDestroyAPIView):
    """View for listing and updating a single `PidXPath` object"""

    permission_classes = (IsAuthenticated,)

    queryset = PidXpath.objects.all()
    serializer_class = PidXpathSerializer
