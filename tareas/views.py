from django.db.models import Case, When, IntegerField, Count
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tarea
from .serializadores_tarea import SerializadorTarea
from .permisos import EsPropietarioDeLaTarea
from .filtros import FiltroTarea


class VistaConjuntoTareas(viewsets.ModelViewSet):
    serializer_class = SerializadorTarea
    permission_classes = [IsAuthenticated, EsPropietarioDeLaTarea]
    filterset_class = FiltroTarea
    search_fields = ["titulo"]
    ordering_fields = ["fecha_limite", "fecha_creacion", "completada", "prioridad"]

    def get_queryset(self):
        # Solo tareas del usuario autenticado
        queryset = Tarea.objects.filter(usuario=self.request.user)

        # Orden de prioridad real: ALTA(1), MEDIA(2), BAJA(3)
        prioridad_orden = Case(
            When(prioridad=Tarea.Prioridad.ALTA, then=1),
            When(prioridad=Tarea.Prioridad.MEDIA, then=2),
            When(prioridad=Tarea.Prioridad.BAJA, then=3),
            default=4,
            output_field=IntegerField(),
        )

        queryset = queryset.annotate(prioridad_orden=prioridad_orden).order_by("prioridad_orden", "fecha_limite")
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vista_panel_resumen(request):
    tareas_usuario = Tarea.objects.filter(usuario=request.user)

    total = tareas_usuario.count()
    completadas = tareas_usuario.filter(completada=True).count()
    pendientes = total - completadas
    porcentaje_avance = (completadas / total * 100) if total > 0 else 0

    return Response(
        {
            "total_tareas": total,
            "tareas_pendientes": pendientes,
            "tareas_completadas": completadas,
            "porcentaje_avance": round(porcentaje_avance, 2),
        }
    )