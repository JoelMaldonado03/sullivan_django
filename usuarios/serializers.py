# usuarios/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from usuarios.models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # No hace falta declarar campos extras: usa username/password por defecto

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Se requieren 'username' y 'password'.")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password
        )
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")

        # Ejecuta la validación estándar (genera access y refresh)
        data = super().validate(attrs)

        # Añade datos de usuario al payload
        data["usuario"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "rol": user.rol,
        }
        return data
