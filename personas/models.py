
    # # Create your models here.
    # class Persona(models.Model):
    # ROL_CHOICES = [
    #     ('Acudiente', 'Acudiente'),
    #     ('Profesor', 'Profesor'),
    #     ('Administrador', 'Administrador'),
    # ]

    # id_persona = models.AutoField(primary_key=True, db_column='ID_Persona')
    # nombre = models.CharField(max_length=100, db_column='Nombre')
    # apellido = models.CharField(max_length=100, db_column='Apellido')
    # fecha_nacimiento = models.DateField(null=True, blank=True, db_column='Fecha_Nacimiento')
    # direccion = models.CharField(max_length=100, null=True, blank=True, db_column='Direccion')
    # telefono = models.CharField(max_length=15, null=True, blank=True, db_column='Telefono')
    # correo_electronico = models.EmailField(max_length=100, null=True, blank=True, db_column='Correo_Electronico')
    # rol = models.CharField(max_length=20, choices=ROL_CHOICES, db_column='Rol')

    # class Meta:
    #     db_table = 'persona'

    # def __str__(self):
    #     return f"{self.nombre} {self.apellido} ({self.rol})"

from django.db import models
from usuarios.models import Usuario

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

class CursoProfesor(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)

    class Meta:
        db_table = 'curso_profesor'