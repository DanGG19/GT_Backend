from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ConfirmacionCorreo
from django.conf import settings

@api_view(["GET"])
@permission_classes([AllowAny])
def vista_confirmar_correo(request):
    token = request.query_params.get("token")
    
    FRONTEND_URL = getattr(settings, 'URL_FRONTEND', 'http://localhost:5173')

    if not token:
        return redirect(f"{FRONTEND_URL}/confirmacion?estado=error&msg=Token+requerido")

    try:
        confirmacion = ConfirmacionCorreo.objects.select_related("usuario").get(token=token)
    except ConfirmacionCorreo.DoesNotExist:
        return redirect(f"{FRONTEND_URL}/confirmacion?estado=error&msg=Token+invalido")

    if confirmacion.usado:
        return redirect(f"{FRONTEND_URL}/confirmacion?estado=usado")

    usuario = confirmacion.usuario
    usuario.is_active = True
    usuario.save()
    confirmacion.usado = True
    confirmacion.save()

    return redirect(f"{FRONTEND_URL}/confirmacion?estado=ok&user={usuario.username}")