# actividades/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path('curso/<int:curso_id>/', views.actividades_por_curso),
  path('curso/<int:curso_id>/crear/', views.crear_actividad_en_curso),
  path('<int:actividad_id>/detalle/', views.detalle_actividad),
  path('<int:actividad_id>/', views.actividad_update_delete),
  path('entrega/<int:actividad_estudiante_id>/', views.actualizar_entrega),
]
