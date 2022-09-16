from django.views import View
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from todo.forms import TaskUpdateForm
from todo.models import Task

from .weather import scrape_weather


class TaskListView(LoginRequiredMixin, ListView):
    """
    A CBV for showing a list of available tasks.
    """
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    A CBV for creating a new task.
    """
    model = Task
    fields = ["title", "priority"]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateVeiw(LoginRequiredMixin, UpdateView):
    """
    A CBV for updating available tasks.
    """
    model = Task
    success_url = reverse_lazy("todo:task_list")
    form_class = TaskUpdateForm
    template_name = "todo/update_task.html"


class TaskCompleteView(LoginRequiredMixin, View):
    """
    A CBV for marking an available task as completed.
    """
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.completed = True
        object.save()
        return redirect(self.success_url)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    A CBV for deleting an available task.
    """
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@login_required
def get_weather(request, city):
    result = {}
    if not cache.get_many([f'{city}_temp', f'{city}_humidity',
                           f'{city}_wind', f'{city}_description',
                           f'{city}_now_svg']):
        result = scrape_weather(city)
        cache.set_many({
                            f'{city}_temp': result['temp'],
                            f'{city}_humidity': result['humidity'],
                            f'{city}_wind': result['wind'],
                            f'{city}_description': result['description'],
                            f'{city}_now_svg': result['now_svg']
                        })

    cache_result = cache.get_many([
                                    f'{city}_temp', f'{city}_humidity',
                                    f'{city}_wind', f'{city}_description',
                                    f'{city}_now_svg'
                                ])
    result = {
        "temp": cache_result[f"{city}_temp"],
        "humidity": cache_result[f"{city}_humidity"],
        "wind": cache_result[f"{city}_wind"],
        "description": cache_result[f"{city}_description"],
        "now_svg": cache_result[f"{city}_now_svg"],
    }
    return JsonResponse(result)
