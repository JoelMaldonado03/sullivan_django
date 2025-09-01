from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( EstudianteViewSet,  
    acudientes_de_estudiante,
    remover_acudiente_de_estudiante,)

router = DefaultRouter()
router.register(r'', EstudianteViewSet)  # queda como /api/estudiantes/

urlpatterns = [
    path('<int:estudiante_id>/acudientes/', acudientes_de_estudiante, name='acudientes-de-estudiante'),
    path('<int:estudiante_id>/acudientes/<int:persona_id>/', remover_acudiente_de_estudiante),
    path('', include(router.urls)),
]
