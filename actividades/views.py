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

# *** LEE DIRECTO LA TABLA RELACIÓN ***
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
    qs = (ActividadEstudiante.objects
          .select_related('estudiante')
          .filter(actividad_id=actividad_id))
    if estado == 'entregadas':
        qs = qs.exclude(entregado_en__isnull=True)
    elif estado == 'pendientes':
        qs = qs.filter(entregado_en__isnull=True)

    ser = ActividadEntregaSerializer(qs.order_by('id'), many=True, context={'request': request})
    return Response(ser.data)

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
    form-data:
      entregable: <archivo>
    Al subir, si no hay 'entregado_en', lo marca con now().
    """
    ae = get_object_or_404(ActividadEstudiante, pk=actividad_estudiante_id)
    archivo = request.FILES.get('entregable')
    if not archivo:
        return Response({'detail': "Falta archivo 'entregable'."}, status=400)

    ae.entregable = archivo
    if ae.entregado_en is None:
        ae.entregado_en = now()
    ae.save()

    return Response(ActividadEntregaSerializer(ae, context={'request': request}).data, status=200)

# === NUEVO ===
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matriz_calificaciones_curso(request, curso_id: int):
    """
    Devuelve en una sola llamada:
    {
      "actividades": [{id, titulo, fecha}, ...],
      "estudiantes": [{id, nombre, apellido}, ...],
      "celdas": [
        {
          "actividad_id": 21,
          "estudiante_id": 11,
          "actividad_estudiante_id": 123,
          "calificacion": "4.5",
          "entregado_en": "2025-09-13T00:39:37Z",
          "entregable_url": "http://.../media/entregables/..."
        }, ...
      ]
    }
    ?todas=1 para incluir actividades de otros profesores del curso.
    """
    todas = request.query_params.get('todas') == '1'

    acts_qs = Actividad.objects.filter(asignada_por__curso_id=curso_id)
    if not todas:
        try:
            profesor = request.user.persona
            acts_qs = acts_qs.filter(asignada_por__persona=profesor)
        except Exception:
            return Response({'detail': 'No asociado a persona.'}, status=400)

    actividades = list(acts_qs.order_by('fecha','id').values('id','titulo','fecha'))
    estudiantes = list(Estudiante.objects.filter(curso_id=curso_id).values('id','nombre','apellido'))

    rel_qs = (ActividadEstudiante.objects
              .select_related('actividad','estudiante')
              .filter(actividad_id__in=[a['id'] for a in actividades]))

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

    return Response({
        'actividades': actividades,
        'estudiantes': estudiantes,
        'celdas': celdas,
    })
