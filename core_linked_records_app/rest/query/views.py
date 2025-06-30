""" REST views for the query API
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_linked_records_app.utils.query import execute_local_pid_query


@extend_schema(
    tags=["PID"],
    description="Retrieve list of PIDs given a query",
)
class RetrieveQueryPidListView(APIView):
    """Retrieve list of PIDs given a query"""

    @extend_schema(
        summary="Retrieve PIDs for a query",
        description="Retrieve list of PIDs given a query",
        request=OpenApiTypes.OBJECT,
        responses={
            200: OpenApiResponse(description="List of PIDs"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        try:
            return Response(
                execute_local_pid_query(request.data, request),
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                f"An unexpected error occured while retrieving PID list: {str(exc)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
