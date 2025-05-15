from django.urls import path, include
from rest_framework import routers
from task import views


# api versioning
routers = routers.DefaultRouter()
routers.register(r'tasks', views.TaskView, 'tasks')

urlpatterns = [
    path("api/v1/", include(routers.urls))
]