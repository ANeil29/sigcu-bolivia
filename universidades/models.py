from django.db import models                 
from simple_history.models import HistoricalRecords


class Universidad(models.Model):
    nombre       = models.CharField(max_length=200)
    sigla        = models.CharField(max_length=20)
    departamento = models.CharField(max_length=100)
    rector       = models.CharField(max_length=200, blank=True)
    telefono     = models.CharField(max_length=50, blank=True)
    website      = models.URLField(blank=True)
    activa       = models.BooleanField(default=True)
    history      = HistoricalRecords()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'
        ordering = ['sigla']

    def __str__(self):
        return f"{self.sigla} — {self.nombre}"


class Facultad(models.Model):
    universidad = models.ForeignKey(
        Universidad, on_delete=models.CASCADE, related_name='facultades'
    )
    nombre   = models.CharField(max_length=200)
    sigla    = models.CharField(max_length=30, blank=True)
    decano   = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    history  = HistoricalRecords()

    class Meta:
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'
        ordering = ['universidad', 'nombre']

    def __str__(self):
        return f"{self.nombre} — {self.universidad.sigla}"


class Sede(models.Model):
    TIPO_CHOICES = [
        ('CENTRAL',   'Central'),
        ('EXTENSION', 'Extensión'),
        ('SEDE',      'Sede'),
    ]

    facultad     = models.ForeignKey(
        Facultad, on_delete=models.CASCADE, related_name='sedes'
    )
    nombre       = models.CharField(max_length=200)
    tipo         = models.CharField(max_length=15, choices=TIPO_CHOICES)
    departamento = models.CharField(max_length=100)
    ciudad       = models.CharField(max_length=100)
    direccion    = models.TextField(blank=True)
    telefono     = models.CharField(max_length=80, blank=True)

    # ── Georreferenciación ────────────────────────────────────────────────────
    # Se usan dos FloatField simples en lugar de PointField (GeoDjango).
    # Leaflet.js consume estos valores directamente para colocar el marcador
    # en el mapa. Ejemplo de valores para Potosí: latitud=-19.5836, longitud=-65.7531
    latitud  = models.FloatField(null=True, blank=True,
                                  help_text='Coordenada Y (ej: -19.5836 para Potosí)')
    longitud = models.FloatField(null=True, blank=True,
                                  help_text='Coordenada X (ej: -65.7531 para Potosí)')

    activa  = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ['departamento', 'ciudad']

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

    @property
    def tiene_coordenadas(self):
        """Devuelve True si la sede tiene latitud y longitud registradas."""
        return self.latitud is not None and self.longitud is not None

    def as_geojson_feature(self):
        """
        Devuelve la sede como diccionario GeoJSON Feature.
        Útil para construir la respuesta del endpoint /sedes/geojson/.
        Devuelve None si la sede no tiene coordenadas.
        """
        if not self.tiene_coordenadas:
            return None
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitud, self.latitud],  
            },
            'properties': {
                'id':          self.pk,
                'nombre':      self.nombre,
                'tipo':        self.get_tipo_display(),
                'facultad':    self.facultad.nombre,
                'universidad': self.facultad.universidad.sigla,
                'ciudad':      self.ciudad,
                'departamento': self.departamento,
                'telefono':    self.telefono,
                'direccion':   self.direccion,
            },
        }