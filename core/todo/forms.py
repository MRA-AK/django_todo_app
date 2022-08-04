from django import forms

from todo.models import Task


class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude  = ['user',]
