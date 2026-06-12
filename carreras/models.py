from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Carrera(models.Model):
    GRADO = [
        ('LIC', 'Licenciatura'),
        ('TUS', 'Técnico Univ. Superior'),
        ('TEC', 'Técnico'),
        ('OTRO', 'Otro'),
    ]
    TIPO = [
        ('C', 'Carrera'),
        ('D', 'Departamento/Programa'),
    ]
    ENFOQUE = [
        ('OBJETIVOS',     'Por Objetivos'),
        ('COMPETENCIAS',  'Por Competencias'),
        ('OTRO',          'Otro'),
    ]

    sede               = models.ForeignKey('universidades.Sede', on_delete=models.PROTECT,
                                           related_name='carreras')
    nombre             = models.CharField(max_length=300)
    programa           = models.CharField(max_length=300, blank=True)
    area               = models.IntegerField(help_text='Área del conocimiento 1-5 según SUB')
    grado              = models.CharField(max_length=5, choices=GRADO)
    tipo               = models.CharField(max_length=2, choices=TIPO)
    diploma_academico  = models.CharField(max_length=300, blank=True)
    titulo_profesional = models.CharField(max_length=300, blank=True)
    enfoque_curricular = models.CharField(max_length=15, choices=ENFOQUE, blank=True)
    en_funcionamiento  = models.BooleanField(default=True)
    numero_sub         = models.IntegerField(null=True, blank=True,
                                             help_text='Número correlativo nacional SUB')
    observaciones      = models.TextField(blank=True)
    history            = HistoricalRecords()
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.nombre} — {self.sede.ciudad}"

    @property
    def estado_rediseno(self):
        ultimo = self.procesos.filter(
            tipo_proceso='REDISENO', estado='CONCLUIDO'
        ).order_by('-anio_conclusion').first()
        if not ultimo or not ultimo.anio_conclusion:
            return 'SIN_DATOS'
        anios = timezone.now().year - ultimo.anio_conclusion
        if anios > 10:
            return 'VENCIDO'
        elif anios >= 8:
            return 'PROXIMO'
        else:
            return 'VIGENTE'

    @property
    def anios_desde_ultimo_rediseno(self):
        ultimo = self.procesos.filter(
            tipo_proceso='REDISENO', estado='CONCLUIDO'
        ).order_by('-anio_conclusion').first()
        if ultimo and ultimo.anio_conclusion:
            return timezone.now().year - ultimo.anio_conclusion
        return None


class PlanEstudio(models.Model):
    carrera           = models.ForeignKey(Carrera, on_delete=models.CASCADE,
                                          related_name='planes_estudio')
    anio_aprobacion   = models.IntegerField()
    evento_aprobacion = models.CharField(max_length=100, blank=True)
    resolucion_hcu    = models.CharField(max_length=100, blank=True)
    resolucion_ran    = models.CharField(max_length=100, blank=True)
    activo            = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Plan de Estudio'
        verbose_name_plural = 'Planes de Estudio'
        ordering            = ['-anio_aprobacion']

    def __str__(self):
        return f"{self.carrera.nombre} — Plan {self.anio_aprobacion}"