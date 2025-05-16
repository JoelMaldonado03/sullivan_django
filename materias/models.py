from django.db import models

# Create your models here.
class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True, db_column='ID_Materia')
    nombre_materia = models.CharField(max_length=100, null=True, blank=True, db_column='Nombre_Materia')

    class Meta:
        db_table = 'materia'

    def __str__(self):
        return self.nombre_materia or f"Materia {self.id_materia}"
