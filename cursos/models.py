from django.db import models

# Create your models here.
from django.db import models

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    class Meta:
        db_table = 'curso'

    def __str__(self):
        return self.nombre_curso
