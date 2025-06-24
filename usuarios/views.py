from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PerfilUsuario

@api_view(['POST'])
def registrar_usuario(request):
    nombre = request.data.get('nombre')
    email = request.data.get('email')
    password = request.data.get('password')
    rol = request.data.get('rol')

    if not all([nombre, email, password, rol]):
        return Response({'error': 'Todos los campos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'El correo ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

    # Crear usuario y perfil
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=nombre
    )
    PerfilUsuario.objects.create(user=user, rol=rol)

    return Response({'message': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_usuario(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([email, password]):
        return Response({'error': 'Email y contrase�a son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            perfil = PerfilUsuario.objects.get(user=user)
            return Response({
                'usuario': {
                    'id': user.id,
                    'nombre': user.first_name,
                    'email': user.email,
                    'rol': perfil.rol,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contrase�a incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except PerfilUsuario.DoesNotExist:
        return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)
