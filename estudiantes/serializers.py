from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'
        
class EstudianteMiniSerializer(serializers.ModelSerializer):
    curso = serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = [
            'id','nombre','apellido',
            'tipo_documento','numero_documento',
            'telefono','direccion','correo_electronico',
            'curso'
        ]

    def get_curso(self, obj):
        c = getattr(obj, 'curso', None)
        if not c: return None
        return {'id': c.id, 'nombre_curso': getattr(c, 'nombre_curso', str(c))}