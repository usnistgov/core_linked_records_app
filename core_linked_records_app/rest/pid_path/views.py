""" REST views for PidPath collection
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser

from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.rest.pid_path.serializers import (
    PidPathSerializer,
)


@extend_schema(
    tags=["PID"],
    description="View for listing and creating `PidPath` objects",
)
class PidPathListView(ListCreateAPIView):
    """View for listing and creating `PidPath` objects"""

    permission_classes = (IsAdminUser,)
    queryset = PidPath.objects.all()
    serializer_class = PidPathSerializer

    @extend_schema(
        summary="Get all PidPath objects",
        description="Get all PidPath objects",
        responses={
            200: PidPathSerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        """Get PidPath list

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new PidPath object",
        description="Create a new PidPath object",
        request=PidPathSerializer,
        responses={
            201: PidPathSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """Create PidPath

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["PID"],
    description="View for retrieving, updating and deleting a single `PidPath` object",
)
class PidPathDetailView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting a single `PidPath` object"""

    permission_classes = (IsAdminUser,)
    queryset = PidPath.objects.all()
    serializer_class = PidPathSerializer

    @extend_schema(
        summary="Retrieve a PidPath object",
        description="Retrieve a PidPath object",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="PidPath ID",
            ),
        ],
        responses={
            200: PidPathSerializer,
            404: OpenApiResponse(description="Object was not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        """Get PidPath

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a PidPath object",
        description="Update a PidPath object",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="PidPath ID",
            ),
        ],
        request=PidPathSerializer,
        responses={
            200: PidPathSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Object was not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        """Update PID path

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a PidPath object",
        description="Partially update a PidPath object",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="PidPath ID",
            ),
        ],
        request=PidPathSerializer,
        responses={
            200: PidPathSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Object was not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        """Update PidPath

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a PidPath object",
        description="Delete a PidPath object",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="PidPath ID",
            ),
        ],
        responses={
            204: None,
            404: OpenApiResponse(description="Object was not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        """Delete PidPath

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        return super().delete(request, *args, **kwargs)
