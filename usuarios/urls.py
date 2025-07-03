# usuarios/urls.py
from django.urls import path
from .views import CustomTokenObtainPairView, register_user

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'', CustomTokenObtainPairView)
urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # …otras rutas…
]
