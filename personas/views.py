from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import CursoProfesor, Persona
from .serializers import PersonaSerializer
from cursos.models import Curso
from cursos.serializers import CursoSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

@api_view(['GET'])
def obtener_cursos_por_profesor(request, id_profesor):
    try:
        cursos = Curso.objects.filter(cursoprofesor__persona_id=id_profesor)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)  
    except Persona.DoesNotExist:
        return Response({"detail": "Profesor no encontrado"}, status=404)
    
@api_view(['POST'])
def agregar_cursos_a_profesor(request, id_profesor):
    try:
        # Obtener al profesor por su ID
        profesor = Persona.objects.get(id=id_profesor)
        
        # Obtener el ID del curso desde el body de la petición
        curso_id = request.data.get('curso_id')
        
        # Obtener el curso
        curso = Curso.objects.get(id=curso_id)
        
        # Crear la relación en la tabla intermedia
        CursoProfesor.objects.create(persona=profesor, curso=curso)
        
        return Response({"detail": "Curso asociado al profesor exitosamente."}, status=status.HTTP_201_CREATED)
    
    except Persona.DoesNotExist:
        return Response({"detail": "Profesor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Curso.DoesNotExist:
        return Response({"detail": "Curso no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def eliminar_curso_de_profesor(request, id_profesor, id_curso):
    try:
        # Obtener el curso asociado al profesor
        curso_profesor = CursoProfesor.objects.get(persona_id=id_profesor, curso_id=id_curso)
        
        # Eliminar la relación
        curso_profesor.delete()
        
        return Response({"detail": "Curso eliminado del profesor exitosamente."}, status=status.HTTP_204_NO_CONTENT)
    
    except CursoProfesor.DoesNotExist:
        return Response({"detail": "La relación entre el profesor y el curso no existe."}, status=status.HTTP_404_NOT_FOUND)