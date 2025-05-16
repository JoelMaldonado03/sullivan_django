from django.db import models
from estudiantes.models import Estudiante
from cursos.models import Curso
from materias.models import Materia

class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True, db_column='ID_Clase')
    fecha = models.DateField(null=True, blank=True, db_column='Fecha')
    asistencia = models.CharField(max_length=10, null=True, blank=True, db_column='Asistencia')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True, db_column='ID_Estudiante')
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, db_column='ID_Curso')
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, db_column='ID_Materia')

    class Meta:
        db_table = 'clase'

