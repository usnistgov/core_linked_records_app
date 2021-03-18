""" REST views for the blob API
"""
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
)
from rest_framework.response import Response

from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.blob.watch import set_blob_pid
from core_linked_records_app.components.local_id import api as local_id_api
from core_main_app.commons.exceptions import CoreError, DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.rest.blob.views import BlobList
from signals_utils.signals.mongo import signals, connector


class BlobUploadWithPID(BlobList):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        """Upload a Blob with a PID. Available only for superusers.

        Args:
            request: HTTP request

        Returns:

            - code: 200
              content: Created blob
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            return Response(
                {"message": "Only a superuser can use this feature."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            if "pid" not in request.POST:
                raise CoreError("Missing PID field in POST data.")

            # Check that the PID has not yet been assigned
            try:
                local_id_api.get_by_name("/".join(request.POST["pid"].split("/")[-2:]))
                raise CoreError("PID has already been assigned.")
            except DoesNotExist:
                pass

            # Upload the blob and return the error if there is one.
            blob_upload_response = super().post(request)

            if blob_upload_response.status_code != status.HTTP_201_CREATED:
                return blob_upload_response

            serialized_data = blob_upload_response.data
            serialized_data["pid"] = request.POST["pid"]

            # Assign PID to blob
            blob_api.set_pid_for_blob(serialized_data["id"], serialized_data["pid"])

            # Return the serialized data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)