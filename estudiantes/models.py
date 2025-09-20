from django.db import models
from cursos.models import Curso

class Estudiante(models.Model):
    TIPO_DOC_CHOICES = (
        ('RC', 'Registro Civil'),
        ('TI', 'Tarjeta de Identidad'),
    )
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo_electronico = models.EmailField(null=True, blank=True)
    tipo_documento = models.CharField(
        max_length=10, choices=TIPO_DOC_CHOICES, null=True, blank=True
    )
    numero_documento = models.CharField(max_length=30, null=True, blank=True)
    foto = models.ImageField(upload_to='avatars/estudiantes/', null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        db_table = 'estudiante'
        indexes = [
            models.Index(fields=['tipo_documento', 'numero_documento']),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
