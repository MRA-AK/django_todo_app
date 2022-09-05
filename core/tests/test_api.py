import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="test", password="testing1234"
    )
    return user


@pytest.mark.django_db
class TestTasksAPI:
    """ Testing todo tasks api """
    def test_get_tasks_with_unauthorized_user_401_status(self, api_client):
        """ Getting tasks with unauthorized user """
        url = reverse("todo:api_v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401
    
    def test_create_task_with_unauthorized_user_401_status(self, api_client):
        """ Creating a task with unauthorized user """
        url = reverse("todo:api_v1:task-list")
        task = {
            "title": "Test task",
            "priority": 1,
            "completed": False
        }
        response = api_client.post(url, task)
        assert response.status_code == 401
    
    def test_get_tasks_response_200_status(self, api_client, common_user):
        """ Getting tasks with authorized user """
        url = reverse("todo:api_v1:task-list")
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200
    
    def test_create_tasks_response_201_status(self, api_client, common_user):
        """ Creating a task with authorized user """
        url = reverse("todo:api_v1:task-list")
        api_client.force_authenticate(user=common_user)
        task = {
            "title": "Test task",
            "priority": 1,
            "completed": False
        }
        response = api_client.post(url, task)

        created_task = Task.objects.all().last()

        assert response.status_code == 201
        assert created_task.title == "Test task"

    def test_create_task_invalid_data_response_400_status(self, api_client, common_user):
        """ Creating a task with invalid data """
        url = reverse("todo:api_v1:task-list")
        api_client.force_authenticate(user=common_user)
        task = {
            "priority": 1,
            "completed": False
        }
        response = api_client.post(url, task)
        assert response.status_code == 400

    def test_edit_tasks_response_200_status(self, api_client, common_user):
        """ Editing a task with authorized user """
        url = reverse("todo:api_v1:task-list")
        api_client.force_authenticate(user=common_user)
        task = {
            "title": "Test task",
            "priority": 1,
            "completed": False
        }
        # Create
        response = api_client.post(url, task)
        task = {
            "title": "Test task2",
            "priority": 1,
            "completed": False
        }
        created_task = Task.objects.all().last()
        url = reverse("todo:api_v1:task-detail",  kwargs={'pk':created_task.id})
        # Edit
        response = api_client.put(url, task)

        created_task = Task.objects.all().last()

        assert response.status_code == 200
        assert created_task.title == "Test task2"

    def test_delete_tasks_response_204_status(self, api_client, common_user):
        """ Deleting a task with authorized user """
        url = reverse("todo:api_v1:task-list")
        api_client.force_authenticate(user=common_user)
        task = {
            "title": "Test task",
            "priority": 1,
            "completed": False
        }
        # Create
        response = api_client.post(url, task)
        task = {
            "title": "Test task2",
            "priority": 1,
            "completed": False
        }
        created_task = Task.objects.all().last()
        url = reverse("todo:api_v1:task-detail",  kwargs={'pk':created_task.id})
        # Delete
        response = api_client.delete(url, task)

        assert response.status_code == 204
        assert not Task.objects.filter(title="Test task2").exists()
