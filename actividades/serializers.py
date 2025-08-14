# actividades/serializers.py
from rest_framework import serializers
from .models import Actividad, ActividadEstudiante

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id','titulo','descripcion','fecha','fecha_entrega','asignada_por']

class ActividadCreateSerializer(serializers.ModelSerializer):
    cpm_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Actividad
        fields = ['id','titulo','descripcion','fecha','fecha_entrega','cpm_id']

    def create(self, validated_data):
        cpm_id = validated_data.pop('cpm_id')
        from personas.models import CursoProfesorMateria
        cpm = CursoProfesorMateria.objects.get(id=cpm_id)
        return Actividad.objects.create(asignada_por=cpm, **validated_data)

class ActividadEntregaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ActividadEstudiante
        fields = ['id','estudiante','estudiante_nombre','entregado_en','calificacion']

    def get_estudiante_nombre(self, obj):
        return f"{obj.estudiante.nombre} {obj.estudiante.apellido}"

class ActividadDetalleSerializer(serializers.ModelSerializer):
    entregas = ActividadEntregaSerializer(many=True, read_only=True)
    class Meta:
        model = Actividad
        fields = ['id','titulo','descripcion','fecha','fecha_entrega','asignada_por','entregas']
