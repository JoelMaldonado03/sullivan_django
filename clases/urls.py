from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClaseViewSet, asistencia_por_clase, marcar_asistencia, marcar_asistencia_bulk

router = DefaultRouter()
router.register(r'', ClaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:clase_id>/asistencia/', asistencia_por_clase, name='asistencia-por-clase'),         # GET
    path('<int:clase_id>/asistencia/marcar/', marcar_asistencia, name='marcar-asistencia'),        # POST
    path('<int:clase_id>/asistencia/bulk/', marcar_asistencia_bulk, name='marcar-asistencia-bulk') # POST
]
