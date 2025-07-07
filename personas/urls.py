from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonaViewSet, mis_cursos, agregar_cursos_a_profesor, eliminar_curso_de_profesor, obtener_cursos_por_profesor


router = DefaultRouter()
router.register(r'', PersonaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cursos/<int:id_profesor>/', obtener_cursos_por_profesor, name='obtener-cursos-profesor'),
    path('cursos/', mis_cursos, name='mis_cursos'),
    path('cursos/<int:id_profesor>/add', agregar_cursos_a_profesor, name='agregar-cursos-profesor'),
    path('cursos/<int:id_profesor>/<int:id_curso>/', eliminar_curso_de_profesor, name='eliminar-curso-profesor'),
]