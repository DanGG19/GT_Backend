from rest_framework import generics, permissions
from .serializadores_usuario import SerializadorRegistroUsuario


class VistaRegistro(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SerializadorRegistroUsuario
