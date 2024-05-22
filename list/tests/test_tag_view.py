from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from list.models import Tag


class TagViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.tag1 = Tag.objects.create(name="home")
        self.tag2 = Tag.objects.create(name="work")
        self.client.login(username="testuser", password="12345")

    def test_tag_list_view(self):
        response = self.client.get(reverse("list:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/tag_list.html")
        self.assertContains(response, self.tag1.name)
        self.assertContains(response, self.tag2.name)

    def test_tag_detail_view(self):
        response = self.client.get(
            reverse("list:tag-detail", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/tag_detail.html")
        self.assertContains(response, self.tag1.name)

    def test_tag_create_view_get(self):
        response = self.client.get(reverse("list:tag-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/generic_form.html")

    def test_tag_create_view_post(self):
        response = self.client.post(reverse("list:tag-create"), {"name": "new tag"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="new tag").exists())

    def test_tag_update_view_get(self):
        response = self.client.get(
            reverse("list:tag-update", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/generic_form.html")

    def test_tag_update_view_post(self):
        response = self.client.post(
            reverse("list:tag-update", kwargs={"pk": self.tag1.pk}),
            {"name": "updated tag"},
        )
        self.assertEqual(response.status_code, 302)
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, "updated tag")

    def test_tag_delete_view_get(self):
        response = self.client.get(
            reverse("list:tag-delete", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list/confirm_delete.html")

    def test_tag_delete_view_post(self):
        response = self.client.post(
            reverse("list:tag-delete", kwargs={"pk": self.tag1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(pk=self.tag1.pk).exists())
