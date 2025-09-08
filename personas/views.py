from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import CursoProfesorMateria, Persona, PersonaEstudiante
from .serializers import PersonaSerializer, CargaEstudiantesSerializer
from asignaciones.serializers import CursoProfesorMateriaSerializer
from cursos.serializers import CursoSerializer
from cursos.models import Curso
from materias.models import Materia
from usuarios.models import Usuario
from estudiantes.models import Estudiante

from openpyxl import load_workbook
import csv, io


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def persona_me(request):
    """
    GET  -> retorna la Persona del usuario
    PATCH -> actualiza parcialmente la Persona (y Usuario anidado si viene)
    """
    try:
        persona = request.user.persona
    except Persona.DoesNotExist:
        return Response({"detail": "Persona no encontrada para este usuario."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(PersonaSerializer(persona).data)

    # PATCH
    serializer = PersonaSerializer(persona, data=request.data, partial=True)
    if serializer.is_valid():
        persona_actualizada = serializer.save()
        return Response(PersonaSerializer(persona_actualizada).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_personas(request):
    """
    GET /personas/buscar?q=texto
    Si q son dígitos -> filtra por numero_documento (icontains)
    Si q tiene texto  -> filtra por nombre/apellido (icontains)
    """
    q = (request.GET.get('q') or '').strip()
    qs = Persona.objects.all()
    if q:
        if q.isdigit():
            qs = qs.filter(numero_documento__icontains=q)
        else:
            qs = qs.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q))
    qs = qs.order_by('apellido','nombre')[:20]
    return Response(PersonaSerializer(qs, many=True).data)



REQUIRED_HEADERS = {
    'curso_id', 'curso_nombre',                 # al menos uno
    'estudiante_nombre', 'estudiante_apellido', 'estudiante_fecha_nacimiento',
    'estudiante_direccion', 'estudiante_telefono', 'estudiante_correo',
    'acudiente_tipo_documento', 'acudiente_numero_documento',
    'acudiente_nombre', 'acudiente_apellido', 'acudiente_telefono',
    'acudiente_direccion', 'acudiente_email',
    'parentesco'
}

def _get_headers_from_ws(ws):
    return [str(c.value).strip() if c.value is not None else '' for c in ws[1]]

def _normalize_headers(headers):
    return [h.strip() for h in headers]

def _row_to_dict(headers, row_values):
    return {headers[i]: (row_values[i] if i < len(row_values) else None) for i in range(len(headers))}

def _read_xlsx(file):
    wb = load_workbook(file, data_only=True)
    ws = wb.active
    headers = _normalize_headers(_get_headers_from_ws(ws))
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        rows.append(_row_to_dict(headers, list(r)))
    return headers, rows

def _read_csv(file):
    text = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(text)
    headers = _normalize_headers(reader.fieldnames or [])
    rows = [ {k.strip(): v for k,v in row.items()} for row in reader ]
    return headers, rows

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def importar_estudiantes(request):
    """
    POST /personas/importar-estudiantes/
    body: multipart/form-data con 'file' (.xlsx o .csv)
    """
    ser = CargaEstudiantesSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    f = ser.validated_data['file']

    # 1) Leer archivo
    ext = (f.name or '').lower()
    if ext.endswith('.xlsx'):
        headers, rows = _read_xlsx(f)
    elif ext.endswith('.csv'):
        headers, rows = _read_csv(f)
    else:
        return Response({'detail':'Formato no soportado. Usa .xlsx o .csv'}, status=400)

    headers_set = set(h for h in headers if h)
    if not (('curso_id' in headers_set) or ('curso_nombre' in headers_set)):
        return Response({'detail':'Debes incluir curso_id o curso_nombre'}, status=400)

    missing = (REQUIRED_HEADERS - headers_set) - {'curso_id','curso_nombre'}
    if missing:
        return Response({'detail': f'Faltan columnas: {sorted(list(missing))}'}, status=400)

    resultado = {
        'procesadas': 0,
        'estudiantes_creados': 0,
        'acudientes_creados': 0,
        'links_creados': 0,
        'errores': []
    }

    # 2) Prefetch de cursos si usas nombre
    cursos_por_nombre = {}
    if 'curso_nombre' in headers_set:
        for c in Curso.objects.all().only('id','nombre_curso'):
            cursos_por_nombre[c.nombre_curso.lower()] = c.id

    # 3) Procesar filas
    for idx, row in enumerate(rows, start=2):  # fila 2 es la primera con datos en Excel
        resultado['procesadas'] += 1
        try:
            with transaction.atomic():
                # Curso
                curso_id = row.get('curso_id')
                curso_nombre = (row.get('curso_nombre') or '').strip()
                if curso_id:
                    curso = get_object_or_404(Curso, id=int(curso_id))
                else:
                    cid = cursos_por_nombre.get(curso_nombre.lower())
                    if not cid:
                        raise ValueError(f"Curso no encontrado: '{curso_nombre}'")
                    curso = Curso.objects.get(id=cid)

                # Acudiente: Usuario (+ Persona)
                a_email = (row.get('acudiente_email') or '').strip()
                a_numdoc = (row.get('acudiente_numero_documento') or '').strip()
                if not a_numdoc:
                    raise ValueError("acudiente_numero_documento es obligatorio")

                persona_acu = Persona.objects.filter(numero_documento=a_numdoc).first()
                if not persona_acu:
                    # crea usuario
                    username = a_email or f"acu_{a_numdoc}"
                    user = Usuario(username=username, email=a_email, rol='Acudiente')
                    # password por defecto: documento (o inutilizable)
                    if a_numdoc:
                        user.set_password(a_numdoc)
                    else:
                        user.set_unusable_password()
                    user.save()

                    persona_acu = Persona.objects.create(
                        usuario=user,
                        nombre=(row.get('acudiente_nombre') or '').strip(),
                        apellido=(row.get('acudiente_apellido') or '').strip(),
                        telefono=(row.get('acudiente_telefono') or '').strip(),
                        tipo_documento=(row.get('acudiente_tipo_documento') or '').strip(),
                        numero_documento=a_numdoc,
                        direccion=(row.get('acudiente_direccion') or '').strip(),
                        fecha_nacimiento=None  # opcional si no viene
                    )
                    resultado['acudientes_creados'] += 1

                # Estudiante
                est = Estudiante.objects.create(
                    nombre=(row.get('estudiante_nombre') or '').strip(),
                    apellido=(row.get('estudiante_apellido') or '').strip(),
                    fecha_nacimiento=row.get('estudiante_fecha_nacimiento') or None,
                    direccion=(row.get('estudiante_direccion') or '').strip(),
                    telefono=(row.get('estudiante_telefono') or '').strip(),
                    correo_electronico=(row.get('estudiante_correo') or '').strip(),
                    nivel_academico='',   # ajusta si tienes ese campo
                    curso_id=curso.id
                )
                resultado['estudiantes_creados'] += 1

                # Link PersonaEstudiante
                PersonaEstudiante.objects.create(
                    persona=persona_acu,
                    estudiante=est,
                    parentesco=(row.get('parentesco') or '').strip() or 'Acudiente'
                )
                resultado['links_creados'] += 1

        except Exception as e:
            resultado['errores'].append({'fila': idx, 'error': str(e)})

    return Response(resultado, status=status.HTTP_200_OK)
