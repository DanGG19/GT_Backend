from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Tarea(models.Model):
    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tareas",
        verbose_name="Usuario",
    )
    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField("Descripción", blank=True)
    prioridad = models.CharField(
        "Prioridad",
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )
    fecha_limite = models.DateField("Fecha límite")
    completada = models.BooleanField("Completada", default=False)
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["-prioridad", "fecha_limite"]

    def clean(self):
        if not self.titulo or not self.titulo.strip():
            raise ValidationError({"titulo": "No se permiten títulos vacíos."})

        hoy = timezone.localdate()
        if self.fecha_limite and self.fecha_limite < hoy:
            raise ValidationError({"fecha_limite": "La fecha límite no puede ser anterior a hoy."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} ({self.prioridad})"