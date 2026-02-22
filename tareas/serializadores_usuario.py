from django.contrib.auth.models import User
from rest_framework import serializers


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
        )
        usuario.set_password(validated_data["password"])
        usuario.save()
        return usuario
