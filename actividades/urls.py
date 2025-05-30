from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActividadViewSet

router = DefaultRouter()
router.register(r'', ActividadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]