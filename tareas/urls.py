from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .vistas_autenticacion import VistaRegistro

urlpatterns = [
    # Auth
    path("registro/", VistaRegistro.as_view(), name="registro"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refrescar/", TokenRefreshView.as_view(), name="token_refrescar"),
]
