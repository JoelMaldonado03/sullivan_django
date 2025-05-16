from django.db import models
from cursos.models import Curso  # asegúrate de tener la app 'cursos'

class Estudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True, db_column='ID_Estudiante')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    apellido = models.CharField(max_length=100, db_column='Apellido')
    fecha_nacimiento = models.DateField(null=True, blank=True, db_column='Fecha_Nacimiento')
    direccion = models.CharField(max_length=100, null=True, blank=True, db_column='Direccion')
    telefono = models.CharField(max_length=15, null=True, blank=True, db_column='Telefono')
    correo_electronico = models.EmailField(max_length=100, null=True, blank=True, db_column='Correo_Electronico')
    nivel_academico = models.CharField(max_length=50, null=True, blank=True, db_column='Nivel_Academico')
    curso = models.ForeignKey(Curso, on_delete=models.SET_DEFAULT, default=1, db_column='ID_Curso')

    class Meta:
        db_table = 'estudiante'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


