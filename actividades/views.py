from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from estudiantes.models import Estudiante
from personas.models import CursoProfesorMateria
from .models import Actividad, ActividadEstudiante
from .serializers import (
    ActividadCreateSerializer,
    ActividadEstudianteSerializer,
    ActividadSerializer,
)



class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer


    def perform_create(self, serializer):
        profesor = self.request.user.persona
        serializer.save(profesor=profesor)





class ActividadesDelProfesorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profesor = getattr(request.user, 'persona', None)
        if not profesor:
            return Response(
                {"detail": "Este usuario no está vinculado a un profesor."},
                status=status.HTTP_400_BAD_REQUEST
            )
        actividades = Actividad.objects.filter(profesor=profesor)
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignar_actividad_a_curso(request):
    """
    Endpoint legacy (sin curso_id en URL): asigna actividad_id a todos
    los estudiantes de curso_id pasado en el body.
    """
    actividad_id = request.data.get("actividad_id")
    curso_id = request.data.get("curso_id")

    if not actividad_id or not curso_id:
        return Response(
            {"detail": "Faltan 'actividad_id' o 'curso_id' en el body."},
            status=status.HTTP_400_BAD_REQUEST
        )

    estudiantes = Estudiante.objects.filter(curso_id=curso_id)
    for estudiante in estudiantes:
        ActividadEstudiante.objects.create(
            actividad_id=actividad_id,
            estudiante=estudiante
        )
    return Response(
        {"detail": "Actividad asignada a todos los estudiantes del curso."}
    )





#Actividades de un estudiante asignadas por el profesor autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_estudiante_y_profesor(request, estudiante_id):
    profesor = request.user.persona
    qs = ActividadEstudiante.objects.filter(
        estudiante_id=estudiante_id,
        actividad__profesor=profesor
    ).select_related('actividad')
    serializer = ActividadEstudianteSerializer(qs, many=True)
    return Response(serializer.data)





#todos los estudiantes del curso actual del profesor con sus actividades
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_curso_y_profesor(request, curso_id=None):
    profesor = request.user.persona

    if curso_id:
        # Verificar que el profesor imparte ese curso
        if not CursoProfesorMateria.objects.filter(
            persona=profesor, curso_id=curso_id
        ).exists():
            return Response(
                {'detail': 'Curso no encontrado o no impartido por este profesor.'},
                status=status.HTTP_404_NOT_FOUND
            )
        cursos_a_consultar = [curso_id]
    else:
        # Todos los cursos del profesor
        cursos_a_consultar = CursoProfesorMateria.objects.filter(
            persona=profesor
        ).values_list('curso_id', flat=True)

    resultado = []
    for cid in cursos_a_consultar:
        estudiantes = Estudiante.objects.filter(curso_id=cid)
        lista_est = []
        for est in estudiantes:
            acts = ActividadEstudiante.objects.filter(
                estudiante=est,
                actividad__profesor=profesor,
                actividad__curso_id=cid
            ).select_related('actividad')
            ser = ActividadEstudianteSerializer(acts, many=True)
            lista_est.append({
                'estudiante_id': est.id,
                'estudiante_nombre': f"{est.nombre} {est.apellido}",
                'actividades': ser.data
            })
        resultado.append({
            'curso_id': cid,
            'estudiantes': lista_est
        })

    return Response({
        'profesor_id': profesor.id,
        'cursos': resultado
    })




#Asignar Actividad a todos los estudiantes de un curso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_y_asignar_actividad(request, curso_id):
    """
    Crea una nueva Actividad (tomando curso_id de la URL y profesor del request.user)
    y la asigna a todos los estudiantes del curso en un solo paso.
    """
    profesor = request.user.persona

    # 1) Verificar permiso
    if not CursoProfesorMateria.objects.filter(
        persona=profesor, curso_id=curso_id
    ).exists():
        return Response(
            {'detail': 'No estás autorizado o el curso no existe.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2) Crear la Actividad
    serializer = ActividadCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    actividad = serializer.save(curso_id=curso_id, profesor=profesor)

    # 3) Bulk-create de asignaciones
    estudiantes = Estudiante.objects.filter(curso_id=curso_id)
    asignaciones = [
        ActividadEstudiante(actividad=actividad, estudiante=est)
        for est in estudiantes
    ]
    ActividadEstudiante.objects.bulk_create(asignaciones)

    return Response({
        'actividad_id': actividad.id,
        'asignadas_a': estudiantes.count()
    }, status=status.HTTP_201_CREATED)