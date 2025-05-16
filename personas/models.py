from django.db import models

# Create your models here.
class Persona(models.Model):
    ROL_CHOICES = [
        ('Acudiente', 'Acudiente'),
        ('Profesor', 'Profesor'),
        ('Administrador', 'Administrador'),
    ]

    id_persona = models.AutoField(primary_key=True, db_column='ID_Persona')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    apellido = models.CharField(max_length=100, db_column='Apellido')
    fecha_nacimiento = models.DateField(null=True, blank=True, db_column='Fecha_Nacimiento')
    direccion = models.CharField(max_length=100, null=True, blank=True, db_column='Direccion')
    telefono = models.CharField(max_length=15, null=True, blank=True, db_column='Telefono')
    correo_electronico = models.EmailField(max_length=100, null=True, blank=True, db_column='Correo_Electronico')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, db_column='Rol')

    class Meta:
        db_table = 'persona'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
