from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


from todo.models import Task
from .serializers import TaskSerializer
from .paginations import DefaultPagination


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['completed', 'priority']
    search_fields = ['title']
    pagination_class = DefaultPagination

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(user=self.request.user)