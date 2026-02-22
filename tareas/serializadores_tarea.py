from django.utils import timezone
from rest_framework import serializers
from .models import Tarea


class SerializadorTarea(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = [
            "id",
            "titulo",
            "descripcion",
            "prioridad",
            "fecha_limite",
            "completada",
            "fecha_creacion",
        ]
        read_only_fields = ["id", "fecha_creacion"]

    def validate_titulo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("No se permiten títulos vacíos.")
        return value

    def validate_fecha_limite(self, value):
        hoy = timezone.localdate()
        if value < hoy:
            raise serializers.ValidationError("La fecha límite no puede ser anterior a hoy.")
        return value