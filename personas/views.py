from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Persona
from .serializers import PersonaSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer