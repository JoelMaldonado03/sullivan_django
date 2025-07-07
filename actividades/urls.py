from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActividadViewSet, ActividadesDelProfesorView, actividades_por_curso_y_profesor, actividades_por_estudiante_y_profesor, asignar_actividad_a_curso

router = DefaultRouter()
router.register(r'', ActividadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mis-actividades/', ActividadesDelProfesorView.as_view(), name='actividades-del-profesor'),
    path('estudiante/<int:estudiante_id>/', actividades_por_estudiante_y_profesor),
    
    path('profesor/cursos/<int:curso_id>/asignar-actividad/', asignar_actividad_a_curso, name='asignar-actividad-a-curso'),

    #Actividades asignadas por el profesor  por cursos
    path('profesor/cursos/',actividades_por_curso_y_profesor,name='actividades-por-todos-los-cursos'),
    # Para un curso concreto
    path('profesor/cursos/<int:curso_id>/', actividades_por_curso_y_profesor, name='actividades-por-curso')
]