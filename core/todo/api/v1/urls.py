from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

app_name = 'api_v1'

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')

urlpatterns = router.urls
