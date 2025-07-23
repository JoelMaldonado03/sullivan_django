from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from cursos.serializers import CursoSerializer
from estudiantes.serializers import EstudianteSerializer
from .models import Clase
from .serializers import ClaseSerializer
from cursos.models import Curso
from estudiantes.models import Estudiante

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer


    @action(detail=False, methods=['get'], url_path='profesor/(?P<profesor_id>[^/.]+)')
    def clases_del_profesor(self, request, profesor_id=None):
        cursos = Curso.objects.filter(profesor__id=profesor_id)
        return Response(CursoSerializer(cursos, many=True).data)


    @action(detail=False, methods=['get'], url_path='estudiantes-del-curso/(?P<curso_id>[^/.]+)')
    def estudiantes_del_curso(self, request, curso_id=None):
        estudiantes = Estudiante.objects.filter(curso__id=curso_id)
        return Response(EstudianteSerializer(estudiantes, many=True).data)
