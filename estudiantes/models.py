from django.db import models
from cursos.models import Curso  

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo_electronico = models.EmailField(null=True, blank=True)
    nivel_academico = models.CharField(max_length=50, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        db_table = 'estudiante'
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


