# actividades/models.py
from django.db import models
from estudiantes.models import Estudiante
from cursos.models import Curso
from personas.models import Persona

class Actividad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='actividades')
    profesor = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'actividad'

    def __str__(self):
        return f"{self.titulo} - {self.curso}"
    

class ActividadEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    entrega = models.BooleanField(default=False)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'actividad')  # Evita duplicados
        db_table = 'actividad_estudiante'

    def __str__(self):
        return f"{self.estudiante} - {self.actividad}"
