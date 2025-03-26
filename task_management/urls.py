from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,UserViewSet

# Create a router for our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet),
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

