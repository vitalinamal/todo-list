from django import forms

from list.models import Task, Tag


class TaskCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "tags":
                field.widget.attrs["class"] = "form-control mb-3"
        self.fields["completed"].widget.attrs["class"] = "form-check-input ml-3"


class TagCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-3"}),
        }
