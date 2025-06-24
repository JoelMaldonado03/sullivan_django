from django.contrib import admin
from .models import PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Permite mostrar el perfil directamente en la vista del User
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

# Extiende el UserAdmin para incluir el PerfilUsuario
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_select_related = ('perfilusuario',)

    def get_rol(self, instance):
        return instance.perfilusuario.rol
    get_rol.short_description = 'Rol'

# Desregistra el admin por defecto y lo registra con el nuevo
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
