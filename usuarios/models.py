from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ("Administrador", "Administrador"),
        ("Profesor", "Profesor"),
        ("Acudiente", "Acudiente"),
    ])

    class Meta:
        db_table = 'perfil_usuario'


    def __str__(self):
        return f"{self.username} ({self.rol})"
