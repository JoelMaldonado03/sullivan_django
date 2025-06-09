from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('ID_Usuario', 'Nombre_Usuario', 'email', 'Rol')
    search_fields = ('Nombre_Usuario', 'email')
    list_filter = ('Rol',)
