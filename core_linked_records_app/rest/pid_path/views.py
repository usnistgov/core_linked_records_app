""" REST views for PidPath collection
"""
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.rest.pid_path.serializers import (
    PidPathSerializer,
)


class PidPathListView(ListCreateAPIView):
    """View for listing and creating `PidPath` objects"""

    permission_classes = (IsAuthenticated,)

    queryset = PidPath.objects.all()
    serializer_class = PidPathSerializer


class PidPathDetailView(RetrieveUpdateDestroyAPIView):
    """View for listing and updating a single `PidPath` object"""

    permission_classes = (IsAuthenticated,)

    queryset = PidPath.objects.all()
    serializer_class = PidPathSerializer
