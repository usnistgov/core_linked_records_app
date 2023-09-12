""" Rest API views to retrieve PID settings
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
)
from core_linked_records_app.rest.pid_settings.serializers import (
    PidSettingsSerializer,
)
from core_linked_records_app.utils.pid import get_pid_settings_dict


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
            pid_settings = pid_settings_api.get(request.user)
            return Response(
                get_pid_settings_dict(pid_settings),
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
            pid_settings_serializer = PidSettingsSerializer(
                data=request.data, context={"request": request}
            )

            if not pid_settings_serializer.is_valid():
                return Response(
                    {"message": "Invalid data provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            pid_settings_serializer.update(
                pid_settings_api.get(request.user),
                pid_settings_serializer.validated_data,
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
