from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .vistas_confirmacion import vista_confirmar_correo


from .vistas_autenticacion import VistaRegistro
from .views import VistaConjuntoTareas, vista_panel_resumen

router = DefaultRouter()
router.register(r"tareas", VistaConjuntoTareas, basename="tareas")

urlpatterns = [
    # Auth
    path("registro/", VistaRegistro.as_view(), name="registro"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refrescar/", TokenRefreshView.as_view(), name="token_refrescar"),

    # API
    path("", include(router.urls)),
    path("panel/", vista_panel_resumen, name="panel_resumen"),

    # Confirmación de correo
    path("confirmar-correo/", vista_confirmar_correo, name="confirmar_correo"),
]