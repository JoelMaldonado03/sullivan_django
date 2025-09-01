from django.urls import path
from . import views

urlpatterns = [
    path('asistencias/cpm/<int:cpm_id>/', views.asistencia_por_cpm_y_fecha),
    path('asistencias/cpm/<int:cpm_id>/upsert/', views.upsert_asistencia),
    path('asistencias/cpm/<int:cpm_id>/fechas/', views.fechas_con_asistencia),
]
