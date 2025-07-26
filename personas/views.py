from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CursoProfesorMateria, Persona
from .serializers import PersonaSerializer
from cursos.models import Curso
from cursos.serializers import CursoSerializer
from materias.models import Materia
from .serializers import CursoProfesorMateriaSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_cursos_por_profesor(request, id_profesor):
    """
    Lista todos los cursos (sin duplicados) asociados al profesor indicado.
    """
    profesor = get_object_or_404(Persona, id=id_profesor)
    # filtramos por la relación intermedia y usamos distinct() para evitar repetir cursos
    cursos = Curso.objects.filter(
        cursoprofesor__persona=profesor
    ).distinct()
    serializer = CursoSerializer(cursos, many=True)
    return Response(serializer.data)
    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_cursos_a_profesor(request, id_profesor):
    """
    Asocia un curso y una materia al profesor.
    Espera en el body JSON:
    {
      "curso_id": <int>,
      "materia_id": <int>
    }
    """
    profesor = get_object_or_404(Persona, id=id_profesor)
    curso_id = request.data.get('curso_id')
    materia_id = request.data.get('materia_id')

    if not curso_id or not materia_id:
        return Response(
            {"detail": "Se requieren 'curso_id' y 'materia_id'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    curso = get_object_or_404(Curso, id=curso_id)
    materia = get_object_or_404(Materia, id=materia_id)

    # get_or_create evita que se duplique la misma terna profesor–curso–materia
    relacion, created = CursoProfesorMateria.objects.get_or_create(
        persona=profesor,
        curso=curso,
        materia=materia
    )

    if created:
        return Response(
            {"detail": "Curso y materia asociados al profesor correctamente."},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"detail": "La relación ya existía."},
            status=status.HTTP_200_OK
        )
    




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_curso_de_profesor(request, id_profesor, id_curso):
    """
    Elimina **todas** las asociaciones curso–profesor (y materias) para ese curso.
    """
    profesor = get_object_or_404(Persona, id=id_profesor)
    qs = CursoProfesorMateria.objects.filter(persona=profesor, curso_id=id_curso)
    deleted_count, _ = qs.delete()

    if deleted_count:
        return Response(
            {"detail": "Se eliminaron las asociaciones del curso correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            {"detail": "No se encontró esa asociación."},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignar_curso_materia_profesor(request):
    serializer = CursoProfesorMateriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_cursos_materias_por_profesor(request, persona_id):
    asignaciones = CursoProfesorMateria.objects.filter(persona_id=persona_id)
    serializer = CursoProfesorMateriaSerializer(asignaciones, many=True)
    return Response(serializer.data)