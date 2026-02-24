from django.contrib.auth.models import User
from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail
from .models import ConfirmacionCorreo

class SerializadorRegistroUsuario(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "username": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo.")
        return value

    def create(self, validated_data):
        usuario = User(
            username=validated_data["username"],
            email=validated_data["email"],
            is_active=False,
        )
        usuario.set_password(validated_data["password"])
        usuario.save()

        confirmacion = ConfirmacionCorreo.objects.create(usuario=usuario)
        enlace = f"{settings.URL_CONFIRMACION_BASE}/api/confirmar-correo/?token={confirmacion.token}"

        asunto = "Confirma tu cuenta - Sistema de Tareas"
        mensaje = (
            f"Hola {usuario.username},\n\n"
            "Gracias por registrarte. Para activar tu cuenta, confirma tu correo entrando al siguiente enlace:\n\n"
            f"{enlace}\n\n"
            "Si no creaste esta cuenta, ignora este correo."
        )

        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )

        return usuario