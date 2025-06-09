from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')            
        email = request.POST.get('email')               
        password = request.POST.get('password')         

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('registro')

        Usuario.objects.create(
            email=email,
            Nombre_Usuario=nombre,
            Contrasena=make_password(password),  # Encriptamos la contraseña
        )
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('login')
    return render(request, 'usuarios/registro.html')


def login_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        clave = request.POST['password']

        try:
            usuario = Usuario.objects.get(Nombre_Usuario=nombre)
            if check_password(clave, usuario.Contrasena):
                request.session['usuario_id'] = usuario.ID_Usuario
                request.session['usuario_nombre'] = usuario.Nombre_Usuario
                return redirect('vista_estudiante')  # o donde lo quieras mandar
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'usuarios/login.html')

def inicio_view(request):
    return render(request, 'usuarios/inicio.html')

def vista_estudiante(request):
    return render(request, 'estudiantes/estudiantes.html')


# Create your views here.
