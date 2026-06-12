from django.db import models
from simple_history.models import HistoricalRecords

class FormularioValoracion(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR',   'Borrador'),
        ('ENVIADO',    'Enviado'),
        ('APROBADO',   'Aprobado'),
        ('OBSERVADO',  'Observado'),
    ]

    proceso          = models.ForeignKey('seguimiento.ProcesoCurricular',
                                         on_delete=models.CASCADE,
                                         related_name='formularios')
    codigo           = models.CharField(max_length=50, unique=True)
    fecha_elaboracion = models.DateField()
    responsable      = models.CharField(max_length=200, blank=True)
    estado           = models.CharField(max_length=15, choices=ESTADO_CHOICES,
                                         default='BORRADOR')
    observaciones    = models.TextField(blank=True)
    archivo_adjunto  = models.FileField(upload_to='formularios/', null=True, blank=True)
    history          = HistoricalRecords()
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Formulario de Valoración'
        verbose_name_plural = 'Formularios de Valoración'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.codigo} — {self.proceso.carrera.nombre}"