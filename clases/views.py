from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Clase
from .serializers import ClaseSerializer

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
