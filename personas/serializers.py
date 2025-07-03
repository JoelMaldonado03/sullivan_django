from rest_framework import serializers
from .models import Persona

class PersonaSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='usuario.rol', read_only=True)

    class Meta:
        model = Persona
        fields = [
            'id',
            'nombre',
            'apellido',
            'telefono',
            'tipo_documento',
            'numero_documento',
            'direccion',
            'fecha_nacimiento',
            'rol'  # <-- este es el campo extra que viene del modelo Usuario
        ]
