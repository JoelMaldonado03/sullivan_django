from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import CursoProfesorMateria, Persona
from .serializers import PersonaSerializer, CursoProfesorMateriaSerializer
from cursos.models import Curso
from cursos.serializers import CursoSerializer
from materias.models import Materia


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_cursos_profesor(request, persona_id):
    """
    Lista todos los cursos y materias asignadas a un profesor específico.
    GET /personas/{persona_id}/cursos-materias/
    """
    profesor = get_object_or_404(Persona, id=persona_id)
    asignaciones = CursoProfesorMateria.objects.filter(persona=profesor)
    serializer = CursoProfesorMateriaSerializer(asignaciones, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def asignar_curso_materia_profesor(request, persona_id, curso_id, materia_id):
    """
    Asigna curso y materia a un profesor.
    POST /personas/{persona_id}/cursos/{curso_id}/materias/{materia_id}/
    """
    persona = get_object_or_404(Persona, id=persona_id)
    curso = get_object_or_404(Curso, id=curso_id)
    materia = get_object_or_404(Materia, id=materia_id)

    obj, created = CursoProfesorMateria.objects.get_or_create(
        persona=persona,
        curso=curso,
        materia=materia
    )

    serializer = CursoProfesorMateriaSerializer(obj)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def eliminar_curso_profesor(request, persona_id, curso_id, materia_id):
    """
    Elimina la asignación curso-materia de un profesor.
    DELETE /personas/{persona_id}/cursos/{curso_id}/materias/{materia_id}/
    """
    asignacion = CursoProfesorMateria.objects.filter(
        persona_id=persona_id,
        curso_id=curso_id,
        materia_id=materia_id
    ).first()

    if asignacion:
        asignacion.delete()
        return Response(
            {"detail": "Asignación eliminada correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )

    return Response(
        {"detail": "Asignación no encontrada."},
        status=status.HTTP_404_NOT_FOUND
    )