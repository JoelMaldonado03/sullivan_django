# usuarios/urls.py
from django.urls import path
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # …otras rutas…
]
