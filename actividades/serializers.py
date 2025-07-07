from rest_framework import serializers
from .models import Actividad, ActividadEstudiante

class ActividadSerializer(serializers.ModelSerializer):
    # Mostrar el nombre del profesor en un GET, se personaliza el serializer así:
    # profesor_nombre = serializers.CharField(source='profesor.nombre', read_only=True)

    # class Meta:
    #     model = Actividad
    #     fields = ['id', 'titulo', 'descripcion', 'fecha', 'curso', 'profesor', 'profesor_nombre']
    #     read_only_fields = ['profesor']
    
    class Meta:
        model = Actividad
        fields = '__all__'
        read_only_fields = ['profesor']


class ActividadEstudianteSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source='actividad.titulo')
    descripcion = serializers.CharField(source='actividad.descripcion')
    fecha = serializers.DateField(source='actividad.fecha')
    curso = serializers.IntegerField(source='actividad.curso.id')

    class Meta:
        model = ActividadEstudiante
        fields = ['id', 'estudiante', 'actividad', 'titulo', 'descripcion', 'fecha', 'curso']


class ActividadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'fecha']
        read_only_fields = []  # el curso y profesor vienen de la URL y request.user