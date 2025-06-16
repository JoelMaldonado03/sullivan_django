from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        usuario = Usuario.objects.get(email=email)
        # print(usuario.Contrasena)
        if password == usuario.Contrasena:
            return Response({
                "usuario": {
                    "id": usuario.ID_Usuario,
                    "nombre": usuario.Nombre_Usuario,
                    "email": usuario.email,
                    "rol": usuario.Rol
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

def inicio_view(request):
    return render(request, 'usuarios/inicio.html')

def vista_estudiante(request):
    return render(request, 'estudiantes/estudiantes.html')


# Create your views here.
