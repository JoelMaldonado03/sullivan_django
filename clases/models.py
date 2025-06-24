from django.db import models
from estudiantes.models import Estudiante
from cursos.models import Curso
from materias.models import Materia
from personas.models import Persona

class Clase(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    profesor = models.ForeignKey(Persona, on_delete=models.CASCADE)  # Rol: Profesor

    class Meta:
            db_table = 'clase'

    def __str__(self):
        return f"Clase de {self.materia} ({self.curso}) - {self.fecha}"


class Asistencia(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    estado = models.CharField(max_length=12, choices=[("Presente", "Presente"), ("Ausente", "Ausente"), ("Justificado", "Justificado")])
   

    class Meta:
        db_table = 'asistencia'

    def __str__(self):
        return f"{self.estudiante} - {self.estado} ({self.clase.fecha})"