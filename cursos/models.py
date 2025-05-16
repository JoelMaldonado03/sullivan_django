from django.db import models

# Create your models here.
from django.db import models

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True, db_column='ID_Curso')
    nombre_curso = models.CharField(max_length=100, db_column='Nombre_Curso')
    descripcion = models.TextField(null=True, blank=True, db_column='Descripcion')

    class Meta:
        db_table = 'curso'

    def __str__(self):
        return self.nombre_curso
