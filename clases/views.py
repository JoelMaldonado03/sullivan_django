from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from estudiantes.models import Estudiante
from estudiantes.serializers import EstudianteSerializer
from cursos.models import Curso
from cursos.serializers import CursoSerializer
from .models import Clase, Asistencia
from .serializers import (
    ClaseSerializer, 
    AsistenciaReadSerializer, 
    AsistenciaWriteSerializer,
)

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

def _check_profesor(request, clase):
    # opcional: limitar a profesor dueño de la clase
    persona = getattr(request.user, 'persona', None)
    if persona and clase.dictada_por.persona_id != persona.id:
        return False
    return True


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asistencia_por_clase(request, clase_id):
    """
    Devuelve la lista de estudiantes del curso de la clase,
    con su estado de asistencia (o None si no está cargada).
    """
    clase = get_object_or_404(Clase, id=clase_id)
    if not _check_profesor(request, clase):
        return Response({'detail': 'No autorizado'}, status=403)

    curso_id = clase.dictada_por.curso_id
    estudiantes = list(Estudiante.objects.filter(curso_id=curso_id))
    asistencias = Asistencia.objects.filter(clase=clase)
    mapa = {a.estudiante_id: a for a in asistencias}

    data = []
    for e in estudiantes:
        a = mapa.get(e.id)
        data.append({
            'estudiante_id': e.id,
            'estudiante_nombre': f'{e.nombre} {e.apellido}',
            'estado': a.estado if a else None,
            'asistencia_id': a.id if a else None,
        })

    return Response({
        'clase_id': clase.id,
        'asistencia_tomada': clase.asistencia_tomada,
        'estudiantes': data,
        'totales': {'estudiantes': len(estudiantes), 'marcadas': len(asistencias)}
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marcar_asistencia(request, clase_id):
    """
    Upsert de asistencia de UN estudiante:
    body = { "estudiante_id": 12, "estado": "Presente"|"Ausente" }
    """
    clase = get_object_or_404(Clase, id=clase_id)
    if not _check_profesor(request, clase):
        return Response({'detail': 'No autorizado'}, status=403)

    estudiante_id = request.data.get('estudiante_id')
    estado = request.data.get('estado')

    if estado not in ('Presente', 'Ausente') or not estudiante_id:
        return Response({'detail': 'Parámetros inválidos'}, status=400)

    # Validar que el estudiante pertenezca al curso de esa clase
    if not Estudiante.objects.filter(id=estudiante_id, curso_id=clase.dictada_por.curso_id).exists():
        return Response({'detail': 'El estudiante no pertenece al curso'}, status=400)

    obj, created = Asistencia.objects.update_or_create(
        clase=clase, estudiante_id=estudiante_id, defaults={'estado': estado}
    )

    # ¿Ya se completó todo?
    total = Estudiante.objects.filter(curso_id=clase.dictada_por.curso_id).count()
    marcadas = Asistencia.objects.filter(clase=clase).count()
    if marcadas >= total and total > 0 and not clase.asistencia_tomada:
        clase.asistencia_tomada = True
        clase.save(update_fields=['asistencia_tomada'])

    return Response({
        'asistencia_id': obj.id,
        'created': created,
        'estado': obj.estado,
        'asistencia_tomada': clase.asistencia_tomada
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marcar_asistencia_bulk(request, clase_id):
    """
    Upsert masivo:
    body = [{ "estudiante_id": 1, "estado": "Presente" }, ...]
    """
    clase = get_object_or_404(Clase, id=clase_id)
    if not _check_profesor(request, clase):
        return Response({'detail': 'No autorizado'}, status=403)

    items = request.data if isinstance(request.data, list) else request.data.get('items')
    if not isinstance(items, list):
        return Response({'detail': 'Se espera una lista'}, status=400)

    valid_ids = set(
        Estudiante.objects.filter(curso_id=clase.dictada_por.curso_id).values_list('id', flat=True)
    )
    creados = actualizados = 0
    for it in items:
        est = it.get('estudiante_id')
        estd = it.get('estado')
        if est in valid_ids and estd in ('Presente', 'Ausente'):
            _, created = Asistencia.objects.update_or_create(
                clase=clase, estudiante_id=est, defaults={'estado': estd}
            )
            if created: creados += 1
            else: actualizados += 1

    total = Estudiante.objects.filter(curso_id=clase.dictada_por.curso_id).count()
    marcadas = Asistencia.objects.filter(clase=clase).count()
    if marcadas >= total and total > 0 and not clase.asistencia_tomada:
        clase.asistencia_tomada = True
        clase.save(update_fields=['asistencia_tomada'])

    return Response({'creados': creados, 'actualizados': actualizados, 'asistencia_tomada': clase.asistencia_tomada})