from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from list.models import Task, Tag


class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.tag1 = Tag.objects.create(name="home")
        self.task1 = Task.objects.create(
            content="Test task 1", deadline="2024-12-31", completed=False
        )
        self.task1.tags.add(self.tag1)
        self.task2 = Task.objects.create(
            content="Test task 2", deadline="2024-11-30", completed=True
        )
        self.task2.tags.add(self.tag1)
        self.client.login(username="testuser", password="12345")

    def test_task_list_view(self):
        response = self.client.get(reverse("list:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/task_list.html")
        self.assertContains(response, self.task1.content)
        self.assertContains(response, self.task2.content)

    def test_task_create_view_get(self):
        response = self.client.get(reverse("list:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/generic_form.html")

    def test_task_create_view_post(self):
        response = self.client.post(
            reverse("list:task-create"),
            {
                "content": "New task",
                "deadline": "2024-10-10T10:00",
                "completed": False,
                "tags": [self.tag1.id],
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(Task.objects.filter(content="New task").exists())

    def test_task_update_view_get(self):
        response = self.client.get(
            reverse("list:task-update", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/generic_form.html")

    def test_task_update_view_post(self):
        response = self.client.post(
            reverse("list:task-update", kwargs={"pk": self.task1.pk}),
            {
                "content": "Updated task",
                "deadline": "2024-12-31T10:00",
                "completed": True,
                "tags": [self.tag1.id],
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.content, "Updated task")
        self.assertTrue(self.task1.completed)

    def test_task_delete_view_get(self):
        response = self.client.get(
            reverse("list:task-delete", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/confirm_delete.html")

    def test_task_delete_view_post(self):
        response = self.client.post(
            reverse("list:task-delete", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
