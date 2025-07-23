from django.db import models
from django.contrib.auth import get_user_model
from estudiantes.models import Estudiante
from cursos.models import Curso
from materias.models import Materia
from personas.models import Persona, CursoProfesorMateria

User = get_user_model()

class Clase(models.Model):
    fecha      = models.DateField()
    duracion   = models.DurationField(null=True, blank=True)
    dictada_por = models.ForeignKey(
        CursoProfesorMateria,
        on_delete=models.CASCADE,
        related_name='clases',
        null= True,
        blank = True
    )
    class Meta:
        db_table = 'clase'

    def __str__(self):
        return f"{self.dictada_por} el {self.fecha}"


class Asistencia(models.Model):
    estado    = models.CharField(max_length=12)
    clase     = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='asistencias')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias', null=True, blank=True)

    class Meta:
        db_table = 'asistencia'