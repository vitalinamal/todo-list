from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from list.forms import TaskCreateOrUpdateForm, TagCreateOrUpdateForm
from list.models import Tag, Task


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    template_name = "list/tag_list.html"
    paginate_by = 12


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    template_name = "list/tag_detail.html"
    paginate_by = 5
    queryset = Tag.objects.prefetch_related("tasks__tags")


class TagCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Tag
    form_class = TagCreateOrUpdateForm
    template_name = "list/generic_form.html"
    success_url = reverse_lazy("list:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Tag"
        return context


class TagUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Tag
    form_class = TagCreateOrUpdateForm
    template_name = "list/generic_form.html"
    success_url = reverse_lazy("list:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Tag"
        return context


class TagDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Tag
    template_name = "list/confirm_delete.html"
    success_url = reverse_lazy("list:tag-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "list/task_list.html"
    queryset = Task.objects.prefetch_related("tags")
    paginate_by = 5


class TaskCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Task
    form_class = TaskCreateOrUpdateForm
    queryset = Task.objects.prefetch_related("tags")
    template_name = "list/generic_form.html"
    success_url = reverse_lazy("list:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task"
        return context


class TaskUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Task
    form_class = TaskCreateOrUpdateForm
    queryset = Task.objects.prefetch_related("tags")
    template_name = "list/generic_form.html"
    success_url = reverse_lazy("list:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Task"
        return context


class TaskDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Task
    template_name = "list/confirm_delete.html"
    success_url = reverse_lazy("list:task-list")


class CompleteOrUndoTaskView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.completed = not task.completed
        task.save()
        return redirect("list:task-list")
