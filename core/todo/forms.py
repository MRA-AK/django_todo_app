from django import forms

from todo.models import Task


class TaskUpdateForm(forms.ModelForm):
    """
    Form for editing a task.
    """

    class Meta:
        model = Task
        exclude  = ['user',]
