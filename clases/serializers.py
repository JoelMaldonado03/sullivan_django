from rest_framework import serializers
from .models import Asistencia, Clase

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'


class AsistenciaReadSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Asistencia
        fields = ('id', 'estudiante', 'estudiante_nombre', 'estado')

    def get_estudiante_nombre(self, obj):
        return f'{obj.estudiante.nombre} {obj.estudiante.apellido}'


class AsistenciaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ('estudiante', 'estado')  # la clase llega por la URL