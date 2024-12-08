# yourapp/views/user_template_assignment.py

from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import UserTemplateAssignmentSerializer
from ..models import UserTemplateAssignment

class UserTemplateAssignmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all user-template assignments.
    POST: Assign a template to a user within an entity.
    """
    queryset = UserTemplateAssignment.objects.all()
    serializer_class = UserTemplateAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can assign templates

    @swagger_auto_schema(
        operation_summary="List and Create User Template Assignments",
        operation_description="Retrieve a list of all template assignments or assign a new template to a user within an entity.",
        request_body=UserTemplateAssignmentSerializer,
        responses={
            200: openapi.Response(
                description="List of user template assignments.",
                schema=UserTemplateAssignmentSerializer(many=True)
            ),
            201: openapi.Response(
                description="User template assignment created successfully.",
                schema=UserTemplateAssignmentSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate assignment."),
            401: openapi.Response(description="Authentication credentials were not provided."),
            403: openapi.Response(description="Permission denied."),
            500: openapi.Response(description="Server error."),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Assign a template to a user within an entity.
        """
        return super().post(request, *args, **kwargs)


class UserTemplateAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific user-template assignment.
    PUT/PATCH: Update a specific assignment.
    DELETE: Remove a specific assignment.
    """
    queryset = UserTemplateAssignment.objects.all()
    serializer_class = UserTemplateAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can manage assignments

    @swagger_auto_schema(
        operation_summary="Retrieve, Update, or Delete a User Template Assignment",
        operation_description="Retrieve details, update, or delete a specific user-template assignment by its ID.",
        responses={
            200: openapi.Response(
                description="User template assignment details.",
                schema=UserTemplateAssignmentSerializer
            ),
            204: openapi.Response(description="User template assignment deleted successfully."),
            400: openapi.Response(description="Invalid input."),
            401: openapi.Response(description="Authentication credentials were not provided."),
            403: openapi.Response(description="Permission denied."),
            404: openapi.Response(description="Assignment not found."),
            500: openapi.Response(description="Server error."),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Update a user-template assignment.
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update a user-template assignment.
        """
        return super().patch(request, *args, **kwargs)


from rest_framework import generics, permissions


class UserSpecificTemplateAssignmentListView(generics.ListAPIView):
    """
    GET: List template assignments for the authenticated user.
    """
    serializer_class = UserTemplateAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTemplateAssignment.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List Authenticated User's Template Assignments",
        operation_description="Retrieve a list of templates assigned to the authenticated user.",
        responses={
            200: openapi.Response(
                description="List of user's template assignments.",
                schema=UserTemplateAssignmentSerializer(many=True)
            ),
            401: openapi.Response(description="Authentication credentials were not provided."),
            500: openapi.Response(description="Server error."),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve assignments for the authenticated user.
        """
        return super().get(request, *args, **kwargs)
