from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Programa(models.Model):
    ESTADO_CHOICES = [
        ('FORMULACION',  'En Formulación'),
        ('APROBACION',   'En Aprobación'),
        ('IMPLEMENTACION', 'En Implementación'),
        ('SUSPENDIDO',   'Suspendido'),
    ]

    GRADO = [
        ('LIC',  'Licenciatura'),
        ('TUS',  'Técnico Univ. Superior'),
        ('TEC',  'Técnico'),
        ('OTRO', 'Otro'),
    ]

    # Relaciones — igual que Carrera
    sede         = models.ForeignKey(
                       'universidades.Sede',
                       on_delete=models.PROTECT,
                       related_name='programas'
                   )
    nombre       = models.CharField(max_length=300)
    descripcion  = models.TextField(blank=True,
                       help_text='Breve descripción del programa y su objetivo')
    area         = models.IntegerField(
                       help_text='Área del conocimiento 1-5 según SUB')
    grado_previsto = models.CharField(
                       max_length=5, choices=GRADO, blank=True,
                       help_text='Grado al que aspira convertirse cuando sea carrera oficial')
    estado       = models.CharField(
                       max_length=20, choices=ESTADO_CHOICES,
                       default='FORMULACION')

    # Fechas del proceso
    fecha_inicio        = models.DateField(null=True, blank=True)
    fecha_prevista_aprobacion = models.DateField(
                                    null=True, blank=True,
                                    help_text='Fecha estimada para convertirse en carrera oficial')

    # Resoluciones
    resolucion_hcu  = models.CharField(max_length=100, blank=True)
    resolucion_ran  = models.CharField(max_length=100, blank=True)
    numero_sub      = models.IntegerField(
                          null=True, blank=True,
                          help_text='Número SUB si ya tiene asignado')

    responsable     = models.CharField(max_length=200, blank=True,
                          help_text='Docente o comisión responsable del programa')
    observaciones   = models.TextField(blank=True)
    activo          = models.BooleanField(default=True)
    history         = HistoricalRecords()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Programa'
        verbose_name_plural = 'Programas'
        ordering            = ['sede__facultad__universidad__sigla', 'nombre']

    def __str__(self):
        return f"{self.nombre} — {self.sede.ciudad} ({self.get_estado_display()})"

    @property
    def universidad(self):
        return self.sede.facultad.universidad

    @property
    def facultad(self):
        return self.sede.facultad

    @property
    def departamento(self):
        return self.sede.departamento

    @property
    def dias_desde_inicio(self):
        if self.fecha_inicio:
            return (timezone.now().date() - self.fecha_inicio).days
        return None

    @property
    def proximo_a_vencer(self):
        """True si la fecha prevista de aprobación es en menos de 90 días."""
        if self.fecha_prevista_aprobacion:
            dias = (self.fecha_prevista_aprobacion - timezone.now().date()).days
            return dias <= 90
        return False