from django.core.management.base import BaseCommand

from faker import Faker
import random

from django.contrib.auth.models import User
from todo.models import Task

priority_list = ["1", "2", "3"]


class Command(BaseCommand):
    help = "creating five dummy tasks"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # Create a new user
        user = User.objects.create(username=self.fake.name(), password="Test@123456")

        for _ in range(5):
            # Create five dummy tasks
            Task.objects.create(
                user = user,
                title = self.fake.text(max_nb_chars=20),
                priority = random.choice(priority_list),
                completed = random.choice([True, False]),
            )
        print("5 dummy tasks created successfully. \U0001F642")