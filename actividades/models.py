from django.db import models
from clases.models import Clase
# Create your models here.
class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True, db_column='ID_Actividad')
    nota = models.CharField(max_length=1, null=True, blank=True, db_column='Nota')
    descripcion = models.TextField(null=True, blank=True, db_column='Descripcion')
    clase = models.ForeignKey(Clase, on_delete=models.SET_NULL, null=True, db_column='ID_Clase')

    class Meta:
        db_table = 'actividad'

    def __str__(self):
        return f"Actividad clase {self.clase_id}"