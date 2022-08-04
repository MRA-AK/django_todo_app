from django.views import View
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from todo.forms import TaskUpdateForm
from todo.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "priority"]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateVeiw(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task_list")
    form_class = TaskUpdateForm
    template_name = "todo/update_task.html"
    


class TaskCompleteView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.completed = True
        object.save()
        return redirect(self.success_url)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
