from rest_framework import serializers
from .models import Persona, CursoProfesorMateria
from cursos.models import Curso
from materias.models import Materia

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

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nombre_curso']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id', 'nombre']

class CursoProfesorMateriaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = CursoProfesorMateria
        fields = '__all__'