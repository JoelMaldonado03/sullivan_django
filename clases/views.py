# clases/views.py
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from personas.models import CursoProfesorMateria
from estudiantes.models import Estudiante
from .models import Asistencia
from .serializers import AsistenciaSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asistencia_por_cpm_y_fecha(request, cpm_id):
    """Devuelve estudiantes del curso y su asistencia para la fecha dada."""
    cpm = get_object_or_404(CursoProfesorMateria, id=cpm_id)
    fecha = request.GET.get('fecha') or date.today().isoformat()

    # estudiantes del curso
    ests = Estudiante.objects.filter(curso_id=cpm.curso_id).values('id','nombre','apellido')

    # mapa asistencias del día
    asist = {
        (a.estudiante_id): a.estado
        for a in Asistencia.objects.filter(cpm=cpm, fecha=fecha)
    }

    return Response({
        'cpm_id': cpm.id,
        'curso_id': cpm.curso_id,
        'materia_id': cpm.materia_id,
        'fecha': fecha,
        'estudiantes': [
            {
                'estudiante_id': e['id'],
                'nombre': e['nombre'],
                'apellido': e['apellido'],
                'estado': asist.get(e['id'])
            }
            for e in ests
        ]
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upsert_asistencia(request, cpm_id):
    """
    Crea/actualiza la asistencia de UN estudiante.
    body: { "fecha":"YYYY-MM-DD", "estudiante_id": 12, "estado": "Presente|Ausente" }
    """
    cpm = get_object_or_404(CursoProfesorMateria, id=cpm_id)
    fecha = request.data.get('fecha')
    estudiante_id = request.data.get('estudiante_id')
    estado = request.data.get('estado')

    if estado not in ('Presente', 'Ausente'):
        return Response({'detail':'Estado inválido'}, status=400)

    obj, _created = Asistencia.objects.update_or_create(
        cpm=cpm, fecha=fecha, estudiante_id=estudiante_id,
        defaults={'estado': estado}
    )
    return Response(AsistenciaSerializer(obj).data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fechas_con_asistencia(request, cpm_id):
    """Lista de fechas en las que hay asistencia para ese CPM."""
    fechas = (Asistencia.objects
              .filter(cpm_id=cpm_id)
              .order_by('fecha')
              .values_list('fecha', flat=True)
              .distinct())
    return Response({'cpm_id': cpm_id, 'fechas': list(fechas)})
