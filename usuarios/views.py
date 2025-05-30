from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user:
            login(request, user)
            return redirect('inicio')  # O cualquier vista principal
        return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'usuarios/login.html')

def registro_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        email = request.POST['email']
        clave = request.POST['password']
        User.objects.create_user(username=usuario, email=email, password=clave)
        return redirect('login')
    return render(request, 'usuarios/registro.html')

def inicio_view(request):
    return render(request, 'usuarios/inicio.html')


# Create your views here.
