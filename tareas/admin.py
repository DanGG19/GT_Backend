from django.contrib import admin
from .models import Tarea


@admin.register(Tarea)
class AdminTarea(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "prioridad", "fecha_limite", "completada", "fecha_creacion")
    list_filter = ("prioridad", "completada")
    search_fields = ("titulo", "descripcion", "usuario__username")
    ordering = ("fecha_limite",)