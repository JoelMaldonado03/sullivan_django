#actividades/views.py
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from .models import Actividad, ActividadEstudiante
from .serializers import (
    ActividadSerializer,
    ActividadCreateSerializer,
    ActividadDetalleSerializer,
    ActividadEntregaSerializer,
)
from estudiantes.models import Estudiante

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_curso(request, curso_id):
    """
    ?todas=1 -> todas las actividades del curso (todos los profes)
    ?todas=0 (default) -> solo las del profe autenticado
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
    Crea actividad + filas en actividad_estudiante para TODOS los estudiantes del curso.
    """
    ser = ActividadCreateSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    actividad = ser.save()

    # Valida correspondencia curso <-> cpm
    if actividad.asignada_por.curso_id != curso_id:
        actividad.delete()
        return Response({'detail':'cpm_id no corresponde al curso.'}, status=400)

    # Genera relación para cada estudiante
    estudiantes = Estudiante.objects.filter(curso_id=curso_id)
    ActividadEstudiante.objects.bulk_create([
        ActividadEstudiante(actividad=actividad, estudiante=e) for e in estudiantes
    ])

    return Response(ActividadDetalleSerializer(actividad, context={'request': request}).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    data = ActividadDetalleSerializer(actividad, context={'request': request}).data
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def entregas_por_actividad(request, actividad_id):
    """
    GET /api/actividades/actividad/<actividad_id>/entregas/?estado=entregadas|pendientes|todas
    - entregadas: entregado_en IS NOT NULL
    - pendientes: entregado_en IS NULL
    - todas: sin filtro
    """
    estado = (request.query_params.get('estado') or 'entregadas').lower()
    
    # Obtener las entregas de la actividad filtradas según el estado
    qs = ActividadEstudiante.objects.select_related('estudiante').filter(actividad_id=actividad_id)

    if estado == 'entregadas':
        qs = qs.exclude(entregado_en__isnull=True)
    elif estado == 'pendientes':
        qs = qs.filter(entregado_en__isnull=True)

    # Serializar los resultados
    entregas = ActividadEntregaSerializer(qs, many=True, context={'request': request}).data

    # Devolver la respuesta
    return Response(entregas)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def actividad_update_delete(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    if request.method == 'DELETE':
        actividad.delete()
        return Response(status=204)

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
    """
    PATCH JSON: { "entregado_en":"2025-09-13T10:30:00Z", "calificacion": 4.5 }
    """
    ae = get_object_or_404(ActividadEstudiante, pk=actividad_estudiante_id)
    data = {}
    if 'entregado_en' in request.data:
        data['entregado_en'] = request.data['entregado_en']
    if 'calificacion' in request.data:
        data['calificacion'] = request.data['calificacion']
    if not data:
        return Response({'detail':'Nada que actualizar.'}, status=400)

    ser = ActividadEntregaSerializer(ae, data=data, partial=True, context={'request': request})
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data)

@api_view(['POST','PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def subir_entregable(request, actividad_estudiante_id):
    """
    sube el archivo de entregable para la actividad del estudiante.
    """
    ae = get_object_or_404(ActividadEstudiante, pk=actividad_estudiante_id)
    archivo = request.FILES.get('entregable')
    if not archivo:
        return Response({'detail': "Falta archivo 'entregable'."}, status=400)

    # Asignar el archivo
    ae.entregable = archivo
    if ae.entregado_en is None:
        ae.entregado_en = now()  # Marcar como entregado
    ae.save()

    return Response(ActividadEntregaSerializer(ae, context={'request': request}).data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matriz_calificaciones_curso(request, curso_id: int):
    """
    Devuelve las calificaciones de actividades para un curso, las actividades del curso, 
    los estudiantes, y los datos completos de las entregas de los estudiantes.
    """
    todas = request.query_params.get('todas') == '1'

    # Obtener todas las actividades del curso
    acts_qs = Actividad.objects.filter(asignada_por__curso_id=curso_id)
    if not todas:
        try:
            profesor = request.user.persona
            acts_qs = acts_qs.filter(asignada_por__persona=profesor)
        except Exception:
            return Response({'detail': 'No asociado a persona.'}, status=400)

    actividades = list(acts_qs.order_by('fecha', 'id').values('id', 'titulo', 'fecha'))
    estudiantes = list(Estudiante.objects.filter(curso_id=curso_id).values('id', 'nombre', 'apellido'))

    # Filtrar las entregas de las actividades
    rel_qs = ActividadEstudiante.objects.select_related('actividad', 'estudiante').filter(actividad_id__in=[a['id'] for a in actividades])

    celdas = []
    for ae in rel_qs:
        try:
            url = ae.entregable.url if ae.entregable else None
        except Exception:
            url = None
        celdas.append({
            'actividad_id': ae.actividad_id,
            'estudiante_id': ae.estudiante_id,
            'actividad_estudiante_id': ae.id,
            'calificacion': (str(ae.calificacion) if ae.calificacion is not None else None),
            'entregado_en': (ae.entregado_en.isoformat() if ae.entregado_en else None),
            'entregable_url': url,
        })

    # Devolver la respuesta con las actividades, estudiantes y celdas
    return Response({
        'actividades': actividades,
        'estudiantes': estudiantes,
        'celdas': celdas,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def entregas_por_estudiante(request, estudiante_id: int):
    """
    GET /actividades/estudiante/<estudiante_id>/?estado=todas|pendientes|entregadas
    Devuelve las filas de ActividadEstudiante de ese estudiante con datos de la actividad.
    """
    estado = (request.query_params.get('estado') or 'todas').lower()

    # Consultar las entregas de actividades de un estudiante
    qs = ActividadEstudiante.objects.select_related('actividad').filter(estudiante_id=estudiante_id)

    if estado == 'pendientes':
        qs = qs.filter(entregado_en__isnull=True)
    elif estado == 'entregadas':
        qs = qs.filter(entregado_en__isnull=False)

    # Serializar las entregas
    entregas = ActividadEntregaSerializer(qs, many=True, context={'request': request}).data

    # Retornar la respuesta con los datos serializados
    return Response(entregas)