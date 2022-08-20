from django.contrib import admin

from todo.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Show Task model in django admin panel.
    """
    list_display = [
        "title",
        "user",
        "completed",
    ]
    search_fields = ["title"]
    list_filter = ["user", "completed"]
