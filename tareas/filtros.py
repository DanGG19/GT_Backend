import django_filters
from .models import Tarea


class FiltroTarea(django_filters.FilterSet):
    # /api/tareas/?completada=true
    completada = django_filters.BooleanFilter(field_name="completada")

    # /api/tareas/?prioridad=ALTA
    prioridad = django_filters.CharFilter(field_name="prioridad")

    class Meta:
        model = Tarea
        fields = ["completada", "prioridad"]