from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Task

class TaskAPITestCase(TestCase):
    """
    Test suite for the Task Management API.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the API tests.
        """
        cls.client = APIClient()

        # Create test users
        cls.user1 = User.objects.create_user(email="user1@example.com", password="password1", name="User One")
        cls.user2 = User.objects.create_user(email="user2@example.com", password="password2", name="User Two")

        # Create test task
        cls.task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            task_type="feature",
            status="pending"
        )

    def test_create_user(self):
        """
        Test creating a new user via API.
        """
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "name": "New User"
        }
        response = self.client.post("/api/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_create_task(self):
        """
        Test creating a new task via API.
        """
        data = {
            "name": "New Task",
            "description": "Task Description",
            "task_type": "bug",
            "status": "in_progress"
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_assign_task(self):
        """
        Test assigning a task to multiple users.
        """
        data = {"user_ids": [self.user1.id, self.user2.id]}
        response = self.client.post(f"/api/tasks/{self.task.id}/assign/", data, format="json")
        
        self.task.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.assigned_users.count(), 2)

    def test_get_user_tasks(self):
        """
        Test retrieving tasks assigned to a specific user.
        """
        self.task.assigned_users.add(self.user1)

        response = self.client.get(f"/api/tasks/user_tasks/?user_id={self.user1.id}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["assigned_tasks"]), 1)
        self.assertEqual(response.data["assigned_tasks"][0]["name"], self.task.name)
