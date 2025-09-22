# academico/services.py
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db.models import Q
from actividades.models import Actividad, ActividadEstudiante
from personas.models import CursoProfesorMateria
from estudiantes.models import Estudiante
from cursos.models import Curso
from .models import Periodo, Logro
from datetime import date

# Si tienes Asistencia:
try:
    from clases.models import Asistencia
except Exception:
    Asistencia = None

# Si tienes NotaMateriaPeriodo:
try:
    from .models import NotaMateriaPeriodo
except Exception:
    NotaMateriaPeriodo = None

def _redondear_1d(x):
    if x is None:
        return None
    return float(Decimal(x).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

def escala_desempeno(nota):
    if nota is None:
        return ''
    if nota < 3.0: return 'BAJO'
    if nota < 4.0: return 'BÁSICO'
    if nota <= 4.5: return 'ALTO'
    return 'SUPERIOR'

def calcular_boletin_estudiante_periodo(curso_id: int, periodo: Periodo, estudiante_id: int):
    curso = Curso.objects.get(pk=curso_id)
    est = Estudiante.objects.get(pk=estudiante_id, curso=curso)

    # Materias (CPM) del curso
    cpms = (CursoProfesorMateria.objects
            .select_related('materia','persona')
            .filter(curso=curso))

    materias_out = []

    for cpm in cpms:
        # Actividades del cpm dentro del rango del período (tu Actividad NO tiene 'periodo' ni 'peso')
        acts = list(
            Actividad.objects.filter(
                asignada_por=cpm,
                fecha__gte=periodo.fecha_inicio,
                fecha__lte=periodo.fecha_fin
            ).values('id','titulo','fecha')
        )

        # Entregas del estudiante para esas actividades
        ae_qs = (ActividadEstudiante.objects
                 .filter(estudiante=est, actividad_id__in=[a['id'] for a in acts])
                 .select_related('actividad'))

        notas = [float(ae.calificacion) for ae in ae_qs if ae.calificacion is not None]

        # Si existe NotaMateriaPeriodo, úsala como respaldo/observación
        obs_doc = ''
        prom = None
        if NotaMateriaPeriodo:
            nmp = NotaMateriaPeriodo.objects.filter(estudiante=est, cpm=cpm, periodo=periodo).first()
            if nmp:
                obs_doc = nmp.observacion_docente or ''
                if nmp.promedio is not None:
                    prom = float(nmp.promedio)

        if prom is None:
            prom = _redondear_1d(sum(notas)/len(notas)) if notas else None
        else:
            prom = _redondear_1d(prom)

        desempeno = escala_desempeno(prom)

        # Faltas (si tienes Asistencia)
        faltas = 0
        if Asistencia is not None:
            faltas = (Asistencia.objects
                      .filter(
                          estudiante_id=est.id,
                          cpm_id=cpm.id,
                          fecha__gte=periodo.fecha_inicio,
                          fecha__lte=periodo.fecha_fin,
                          estado__iexact='ausente'
                      ).count())

        # Logros con orden+descripcion
        logros_qs = Logro.objects.filter(cpm=cpm, periodo=periodo).order_by('orden')
        logros = [{'orden': lg.orden, 'descripcion': lg.descripcion} for lg in logros_qs]

        materias_out.append({
            'materia_nombre': cpm.materia.nombre,
            'profesor': f"{cpm.persona.nombre} {cpm.persona.apellido}",
            'promedio': prom,
            'desempeno': desempeno,
            'inasistencias': faltas,
            'observacion_docente': obs_doc,
            'logros': logros,
        })

    data = {
        'anio': periodo.anio,
        'generado_el': date.today().isoformat(),
        'curso': {'id': curso.id, 'nombre_curso': curso.nombre_curso},
        'periodo': {
            'id': periodo.id,
            'anio': periodo.anio,
            'numero': periodo.numero,
            'nombre': periodo.nombre,
            'fecha_inicio': periodo.fecha_inicio,
            'fecha_fin': periodo.fecha_fin,
            'activo': periodo.activo,
        },
        'estudiante': {
            'id': est.id,
            'nombre': est.nombre,
            'apellido': est.apellido,
            'tipo_documento': est.tipo_documento,
            'numero_documento': est.numero_documento,
        },
        'materias': materias_out,
        'observaciones_generales': '',
    }
    return data
