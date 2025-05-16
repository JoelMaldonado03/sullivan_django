from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet

router = DefaultRouter()
router.register(r'', EstudianteViewSet)  # queda como /api/estudiantes/

urlpatterns = [
    path('', include(router.urls)),
]
