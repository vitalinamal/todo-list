from django.test import TestCase
from list.forms import TaskCreateOrUpdateForm, TagCreateOrUpdateForm
from list.models import Tag


class TaskCreateOrUpdateFormTest(TestCase):

    def test_form_fields_classes(self):
        form = TaskCreateOrUpdateForm()
        self.assertTrue(
            form.fields["content"].widget.attrs["class"], "form-control mb-3"
        )
        self.assertTrue(
            form.fields["deadline"].widget.attrs["class"], "form-control mb-3"
        )
        self.assertTrue(
            form.fields["completed"].widget.attrs["class"], "form-check-input ml-3"
        )

    def test_valid_data(self):
        tag = Tag.objects.create(name="home")
        form = TaskCreateOrUpdateForm(
            data={
                "content": "Test task content",
                "deadline": "2024-12-31T23:59",
                "completed": False,
                "tags": [tag.id],
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = TaskCreateOrUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


class TagCreateOrUpdateFormTest(TestCase):

    def test_form_fields_classes(self):
        form = TagCreateOrUpdateForm()
        self.assertTrue(form.fields["name"].widget.attrs["class"], "form-control mb-3")

    def test_valid_data(self):
        form = TagCreateOrUpdateForm(data={"name": "Test tag"})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = TagCreateOrUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
