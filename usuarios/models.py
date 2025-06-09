from django.db import models

class Usuario(models.Model):
    ID_Usuario = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=80, unique=True)
    Nombre_Usuario = models.CharField(max_length=50, unique=True)
    Contrasena = models.CharField(max_length=200)
    Rol = models.CharField(
        max_length=30,
        choices=[
            ('Administrador', 'Administrador'),
            ('Profesor', 'Profesor'),
        ]
    )
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.Nombre_Usuario


# Create your models here.
