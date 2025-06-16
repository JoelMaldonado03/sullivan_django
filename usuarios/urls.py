from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login, name='login'),
    path('estudiante/', views.vista_estudiante, name='vista_estudiante'),
    path('inicio/', views.inicio_view, name='inicio'),
]
