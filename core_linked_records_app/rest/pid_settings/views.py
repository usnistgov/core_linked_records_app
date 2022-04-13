""" Rest API views to retrieve PID settings
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app import settings
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.rest.pid_settings.serializers import (
    PidSettingsSerializer,
)


class PidSettingsView(APIView):
    """Retrieve PID settings"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Retrieve the settings for the PID system

        Args:
            request:

        Returns:
        """
        try:
            pid_settings = pid_settings_api.get()
            pid_settings_data = PidSettingsSerializer(pid_settings).data

            response_data = {
                "xpath": settings.PID_XPATH,
                "format": settings.PID_FORMAT,
                "system": settings.ID_PROVIDER_SYSTEM_NAME,
                "prefixes": settings.ID_PROVIDER_PREFIXES,
            }

            pid_settings_data.update(response_data)

            return Response(
                pid_settings_data,
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                {
                    "message": f"An unexpected error occurred while displaying "
                    f"PidSettings: {str(exc)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request):
        """Update settings for the PID system. Current, only works for automatically
        setting PIDs (`auto_set_pid`).

        Args:
            request:

        Returns:
        """
        if not request.user.is_superuser:
            return Response(
                {"message": "Only a superuser can use this feature."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            pid_settings_serializer = PidSettingsSerializer(data=request.data)

            if not pid_settings_serializer.is_valid():
                return Response(
                    {"message": "Invalid data provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            pid_settings_serializer.update(
                pid_settings_api.get(), pid_settings_serializer.validated_data
            )

            return self.get(request)
        except Exception as exc:
            return Response(
                {
                    "message": f"An unexpected error occurred while modifying "
                    f"PidSettings: {str(exc)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
