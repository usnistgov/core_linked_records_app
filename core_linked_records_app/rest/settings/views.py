""" Rest API views to retrieve PID settings
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app import settings


class PidSettings(APIView):
    """Retrieve PID settings"""

    def get(self, request):
        return Response(
            {
                "xpath": settings.PID_XPATH,
                "format": settings.PID_FORMAT,
                "systems": list(settings.ID_PROVIDER_SYSTEMS.keys()),
                "prefixes": settings.ID_PROVIDER_PREFIXES,
                "auto_set": settings.AUTO_SET_PID,
            },
            status=status.HTTP_200_OK,
        )
