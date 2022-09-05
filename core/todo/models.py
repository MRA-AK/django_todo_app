from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Define a Task model in database.
    """
    CHOICES = (
        ('1', 'High'),
        ('2', 'Medium'),
        ('3', 'Low'),
    )

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=50, choices=CHOICES, default=3)
    completed = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
