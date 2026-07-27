from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class TipoFase(models.Model):
    codigo      = models.CharField(max_length=10, unique=True)
    nombre      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    medio_verificacion_default = models.TextField(blank=True)
    orden       = models.IntegerField(default=0)
    activa      = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"

class ProcesoCurricular(models.Model):
    TIPO = [
        ('DISENO', 'Diseño Curricular'),
        ('REDISENO', 'Rediseño Curricular'),
        ('AJUSTE', 'Ajuste Curricular'),
        ('COMPLEMENTACION', 'Complementación Curricular'),
        ('OTRO', 'Otro'),
    ]
    ESTADO = [
        ('EN_PROCESO', 'En Proceso'),
        ('CONCLUIDO', 'Concluido'),
        ('ARCHIVADO', 'Archivado'),
    ]

    carrera        = models.ForeignKey('carreras.Carrera', on_delete=models.CASCADE,
                                       related_name='procesos')
    tipo_proceso   = models.CharField(max_length=20, choices=TIPO)
    nombre_proceso = models.CharField(max_length=300, blank=True)
    anio_inicio    = models.IntegerField()
    anio_conclusion = models.IntegerField(null=True, blank=True)
    estado         = models.CharField(max_length=15, choices=ESTADO, default='EN_PROCESO')
    observaciones  = models.TextField(blank=True)
    history        = HistoricalRecords()

    def __str__(self):
        return f"{self.carrera.nombre} — {self.get_tipo_proceso_display()} {self.anio_inicio}"

    @property
    def anios_desde_conclusion(self):
        if self.anio_conclusion:
            return timezone.now().year - self.anio_conclusion
        return None

class FaseProceso(models.Model):
    ESTADO = [
        ('PENDIENTE',   'Pendiente'),
        ('EN_PROCESO',  'En Proceso'),
        ('COMPLETADO',  'Completado'),
    ]
    proceso            = models.ForeignKey(ProcesoCurricular,
                             on_delete=models.CASCADE, related_name='fases')
    tipo_fase          = models.ForeignKey(TipoFase, on_delete=models.PROTECT)
    fecha_inicio       = models.DateField(null=True, blank=True)
    fecha_conclusion   = models.DateField(null=True, blank=True)
    medio_verificacion = models.TextField(blank=True)
    estado             = models.CharField(max_length=15, choices=ESTADO,
                             default='PENDIENTE')
    observaciones      = models.TextField(blank=True)

    archivo_verificacion = models.FileField(
        upload_to='verificacion_fases/%Y/%m/',
        null=True, blank=True,
        help_text='Sube el documento que verifica esta fase (PDF, Word, Excel)'
    )

    def __str__(self):
        return f"{self.proceso} — Fase: {self.tipo_fase.codigo}"

    @property
    def nombre_archivo(self):
        if self.archivo_verificacion:
            return self.archivo_verificacion.name.split('/')[-1]
        return None

    @property
    def extension_archivo(self):
        if self.archivo_verificacion:
            ext = self.archivo_verificacion.name.split('.')[-1].lower()
            return ext
        return None

    def __str__(self):
        return f"{self.proceso} — Fase: {self.tipo_fase.codigo}"