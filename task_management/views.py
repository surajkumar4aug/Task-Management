from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Task,User
from .serializers import UserSerializer, TaskSerializer, TaskCreateSerializer, TaskAssignSerializer, UserTasksSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.

    Provides CRUD operations for the User model, allowing clients to:
    - List all users: GET /api/users/
    - Retrieve a specific user: GET /api/users/{id}/
    - Create a new user: POST /api/users/
    - Update an existing user: PUT /api/users/{id}/
    - Delete a user: DELETE /api/users/{id}/
    """
    
    queryset = User.objects.all()  
    serializer_class = UserSerializer 

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Validates and saves the user data from the request.
        Endpoint: POST /api/users/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Update an existing user.

        Validates and updates the user data.
        Endpoint: PUT /api/users/{id}/
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a user.

        Removes the user from the database.
        Endpoint: DELETE /api/users/{id}/
        """
        return super().destroy(request, *args, **kwargs)

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tasks.

    Provides CRUD operations for tasks and additional endpoints for:
    - Assigning tasks to users: POST /api/tasks/{id}/assign/
    - Retrieving tasks for a specific user: GET /api/tasks/user_tasks/?user_id={id}
    """
    
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer 

    def get_serializer_class(self):
        """
        Determine the serializer class to use based on the action.

        Returns:
            TaskCreateSerializer: Used for creating new tasks.
            TaskSerializer: Used for other actions (list, retrieve, update, delete).
        """
        if self.action == 'create':
            return TaskCreateSerializer  
        return TaskSerializer 

    def create(self, request, *args, **kwargs):
        """
        Create a new task with name, description, task_type, and status.

        Endpoint: POST /api/tasks/
        """
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Get a list of all tasks.

        Endpoint: GET /api/tasks/
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get details of a specific task by ID.

        Endpoint: GET /api/tasks/{id}/
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=TaskAssignSerializer,
        responses={200:TaskSerializer}
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign a task to one or multiple users.
        Provide a list of user IDs to assign the task to. This will replace any existing assignments.

        Endpoint: POST /api/tasks/{id}/assign/
        """
        task = self.get_object()
        serializer = TaskAssignSerializer(data=request.data)

        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            users = User.objects.filter(id__in=user_ids)

            task.assigned_users.clear()
            task.assigned_users.set(users)

            return Response({
                'status': 'Task assigned successfully',
                'task': TaskSerializer(task).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description="User ID to fetch assigned tasks",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: UserTasksSerializer}  # Correctly using the new serializer
    )
    @action(detail=False, methods=['get'])
    def user_tasks(self, request):
        """
         Get all tasks assigned to a specific user.
         Endpoint: GET /api/tasks/user_tasks/?user_id={id}
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        tasks = user.assigned_tasks.all().order_by('id')  # Order tasks by ID

        response_data = UserTasksSerializer({
            "user": user,
            "assigned_tasks": tasks
        }).data

        return Response(response_data, status=status.HTTP_200_OK)