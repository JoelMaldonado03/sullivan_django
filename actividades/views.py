# actividades/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Actividad, ActividadEstudiante
from .serializers import (
    ActividadSerializer,
    ActividadCreateSerializer,
    ActividadDetalleSerializer,
    ActividadEntregaSerializer,
)
from personas.models import CursoProfesorMateria
from estudiantes.models import Estudiante

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_curso(request, curso_id):
    """
    ?todas=1 para ver actividades de TODOS los profes del curso.
    Por defecto (todas=0), solo las del profe autenticado.
    """
    todas = request.query_params.get('todas') == '1'
    qs = Actividad.objects.filter(asignada_por__curso_id=curso_id)
    if not todas:
        try:
            profesor = request.user.persona
            qs = qs.filter(asignada_por__persona=profesor)
        except Exception:
            return Response({'detail': 'No asociado a persona.'}, status=400)

    data = ActividadSerializer(qs.order_by('-fecha','-id'), many=True).data
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_actividad_en_curso(request, curso_id):
    """
    Body: { titulo, descripcion, fecha, fecha_entrega?, cpm_id }
    Crea la actividad y genera ActividadEstudiante para TODOS los
    estudiantes del curso.
    """
    ser = ActividadCreateSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=400)
    actividad = ser.save()

    # Validación de correspondencia curso <-> cpm
    if actividad.asignada_por.curso_id != curso_id:
        actividad.delete()
        return Response({'detail':'cpm_id no corresponde al curso.'}, status=400)

    # Crear las entregas por estudiante del curso
    estudiantes = Estudiante.objects.filter(curso_id=curso_id)
    asignaciones = [
        ActividadEstudiante(actividad=actividad, estudiante=e)
        for e in estudiantes
    ]
    ActividadEstudiante.objects.bulk_create(asignaciones)

    return Response(ActividadDetalleSerializer(actividad).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    data = ActividadDetalleSerializer(actividad).data
    return Response(data)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def actividad_update_delete(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)

    if request.method == 'DELETE':
        actividad.delete()
        return Response(status=204)

    # PATCH
    partial = {}
    for f in ['titulo','descripcion','fecha','fecha_entrega']:
        if f in request.data:
            partial[f] = request.data[f]
    if not partial:
        return Response({'detail':'Nada que actualizar.'}, status=400)

    ser = ActividadSerializer(actividad, data=partial, partial=True)
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_entrega(request, actividad_estudiante_id):
    ae = get_object_or_404(ActividadEstudiante, pk=actividad_estudiante_id)
    data = {}

    if 'entregado_en' in request.data:
        data['entregado_en'] = request.data['entregado_en']
    if 'calificacion' in request.data:
        data['calificacion'] = request.data['calificacion']

    if not data:
        return Response({'detail':'Nada que actualizar.'}, status=400)

    ser = ActividadEntregaSerializer(ae, data=data, partial=True)
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data)
