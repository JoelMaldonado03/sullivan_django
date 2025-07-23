from django.db import models
from cursos.models import Curso
from usuarios.models import Usuario
from materias.models import Materia

class Persona(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    
    class Meta:
        db_table = 'persona'    

class PersonaEstudiante(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    estudiante = models.ForeignKey('estudiantes.Estudiante', on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=30)

    class Meta:
        db_table = 'persona_estudiante'

class CursoProfesorMateria(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='cursos_profesor')
    curso   = models.ForeignKey(Curso,  on_delete=models.CASCADE, related_name='cursos_profesor')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cursos_profesor')

    class Meta:
        db_table = 'curso_profesor_materia'
        unique_together = (('persona','curso','materia'),)