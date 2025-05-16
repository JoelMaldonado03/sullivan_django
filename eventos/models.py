from django.db import models

# Create your models here.
class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True, db_column='ID_Evento')
    titulo = models.CharField(max_length=255, db_column='Titulo')
    descripcion = models.TextField(null=True, blank=True, db_column='Descripcion')
    fecha_inicio = models.DateTimeField(null=True, blank=True, db_column='Fecha_Inicio')
    fecha_fin = models.DateTimeField(null=True, blank=True, db_column='Fecha_Fin')
    ubicacion = models.CharField(max_length=255, null=True, blank=True, db_column='Ubicacion')

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

class UsuarioEvento(models.Model):
    usuario_id = models.IntegerField(db_column='ID_Usuario')  # reemplazar por FK si tienes modelo Usuario
    evento_id = models.IntegerField(db_column='ID_Evento')

    class Meta:
        db_table = 'usuario_evento'
        unique_together = (('usuario_id', 'evento_id'),)
