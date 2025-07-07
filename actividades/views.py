from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from estudiantes.models import Estudiante
from personas.models import CursoProfesor
from .models import Actividad, ActividadEstudiante
from .serializers import ActividadCreateSerializer, ActividadEstudianteSerializer, ActividadSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

    def perform_create(self, serializer):
        # Asignar automáticamente el profesor basado en el usuario autenticado
        persona = self.request.user.persona  # Asumiendo la  relacion Usuario con Persona
        serializer.save(profesor=persona)



class ActividadesDelProfesorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profesor = request.user.persona  # Relación Usuario -> Persona
        except AttributeError:
            return Response({"detail": "Este usuario no está vinculado a un profesor."}, status=400)

        actividades = Actividad.objects.filter(profesor=profesor)
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignar_actividad_a_curso(request):
    actividad_id = request.data.get("actividad_id")
    curso_id = request.data.get("curso_id")

    estudiantes = Estudiante.objects.filter(curso_id=curso_id)

    for estudiante in estudiantes:
        ActividadEstudiante.objects.create(
            actividad_id=actividad_id,
            estudiante=estudiante
        )

    return Response({"detail": "Actividad asignada a todos los estudiantes del curso."})




#Actividades de un estudiante asignadas por el profesor autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_estudiante_y_profesor(request, estudiante_id):
    profesor = request.user.persona  # profesor autenticado

    actividades = ActividadEstudiante.objects.filter(
        estudiante_id=estudiante_id,
        actividad__profesor=profesor
    ).select_related('actividad')

    serializer = ActividadEstudianteSerializer(actividades, many=True)
    return Response(serializer.data)



#todos los estudiantes del curso actual del profesor con sus actividades
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividades_por_curso_y_profesor(request, curso_id=None):
    profesor = request.user.persona

     # 1) ¿Me piden un curso en concreto?
    if curso_id:
        # Verifico que el profe imparta ese curso
        qs_cp = CursoProfesor.objects.filter(persona=profesor, curso_id=curso_id)
        if not qs_cp.exists():
            return Response(
                {'detail': 'Curso no encontrado o no impartido por este profesor.'},
                status=status.HTTP_404_NOT_FOUND
            )
        cursos_a_consultar = [curso_id]
    else:
        # 2) Si no me pasan id, traigo **todos** los cursos del profe
        cursos_a_consultar = (
            CursoProfesor.objects
            .filter(persona=profesor)
            .values_list('curso_id', flat=True)
        )

    resultado_por_curso = []
    for cid in cursos_a_consultar:
        # 3) estudiantes de ese curso
        estudiantes = Estudiante.objects.filter(curso_id=cid)

        lista_est = []
        for est in estudiantes:
            actividades_qs = ActividadEstudiante.objects.filter(
                estudiante=est,
                actividad__profesor=profesor,
                actividad__curso_id=cid
            ).select_related('actividad')
            ser = ActividadEstudianteSerializer(actividades_qs, many=True)
            lista_est.append({
                'estudiante_id': est.id,
                'estudiante_nombre': f"{est.nombre} {est.apellido}",
                'actividades': ser.data
            })

        resultado_por_curso.append({
            'curso_id': cid,
            'estudiantes': lista_est
        })

    return Response({
        'profesor_id': profesor.id,
        'cursos': resultado_por_curso
    })



#Asignar Actividad a todos los estudiantes de un curso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignar_actividad_a_curso(request, curso_id):
    profesor = request.user.persona

    # 1) Verifico que este profesor imparta ese curso
    if not CursoProfesor.objects.filter(persona=profesor, curso_id=curso_id).exists():
        return Response(
            {'detail': 'No estás autorizado o el curso no existe.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2) Creo la Actividad con curso y profesor implícitos
    serializer = ActividadCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    actividad = serializer.save(curso_id=curso_id, profesor=profesor)

    # 3) Busco todos los estudiantes de ese curso
    estudiantes = Estudiante.objects.filter(curso_id=curso_id)

    # 4) Creo las asignaciones en bloque
    asignaciones = [
        ActividadEstudiante(actividad=actividad, estudiante=est)
        for est in estudiantes
    ]
    ActividadEstudiante.objects.bulk_create(asignaciones)

    return Response({
        'actividad_id': actividad.id,
        # asignadas_a es el número de estudiantes del curso
        'asignadas_a': estudiantes.count()
    }, status=status.HTTP_201_CREATED)