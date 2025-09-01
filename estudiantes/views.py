from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Estudiante
from .serializers import EstudianteSerializer
from personas.models import Persona, PersonaEstudiante
from personas.serializers import PersonaSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def acudientes_de_estudiante(request, estudiante_id):
    """
    GET  /estudiantes/{id}/acudientes/  -> lista acudientes
    POST /estudiantes/{id}/acudientes/  -> asigna acudiente
      body: { "persona_id": 5, "parentesco": "Acudiente" }
    """
    est = get_object_or_404(Estudiante, pk=estudiante_id)

    if request.method == 'GET':
        persona_ids = (PersonaEstudiante.objects
                       .filter(estudiante=est)
                       .values_list('persona_id', flat=True))
        acudientes = Persona.objects.filter(id__in=persona_ids).order_by('apellido','nombre')
        return Response(PersonaSerializer(acudientes, many=True).data)

    # POST
    persona_id = request.data.get('persona_id')
    parentesco = request.data.get('parentesco', 'Acudiente')
    if not persona_id:
        return Response({'detail': 'persona_id es requerido'}, status=400)

    persona = get_object_or_404(Persona, pk=persona_id)
    PersonaEstudiante.objects.get_or_create(
        persona=persona, estudiante=est, defaults={'parentesco': parentesco}
    )

    # devolver lista actualizada
    persona_ids = (PersonaEstudiante.objects
                   .filter(estudiante=est)
                   .values_list('persona_id', flat=True))
    acudientes = Persona.objects.filter(id__in=persona_ids).order_by('apellido','nombre')
    return Response(PersonaSerializer(acudientes, many=True).data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remover_acudiente_de_estudiante(request, estudiante_id, persona_id):
    est = get_object_or_404(Estudiante, pk=estudiante_id)
    PersonaEstudiante.objects.filter(estudiante=est, persona_id=persona_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)