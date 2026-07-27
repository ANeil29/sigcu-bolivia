from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('SUPERADMIN',  'Superadministrador SUB'),
        ('ADMIN_DSA',   'Administrador DSA'),
        ('TECNICO',     'Técnico Curricular'),
        ('DOCENTE',     'Docente'),
        ('ESTUDIANTE',  'Estudiante'),
        ('PENDIENTE',   'Pendiente de aprobación'),
    ]

    CARGO_CHOICES = [
        ('RECTOR',        'Rector'),
        ('VICERRECTOR',   'Vicerrector'),
        ('DECANO',        'Decano'),
        ('DIRECTOR',      'Director de Carrera'),
        ('TECNICO_DSA',   'Técnico DSA'),
        ('DOCENTE',       'Docente'),
        ('ESTUDIANTE',    'Estudiante'),
        ('ADMINISTRATIVO','Administrativo'),
        ('OTRO',          'Otro'),
    ]

    rol            = models.CharField(max_length=20, choices=ROL_CHOICES,
                                      default='PENDIENTE')
    universidad    = models.ForeignKey(
                         'universidades.Universidad',
                         on_delete=models.SET_NULL,
                         null=True, blank=True,
                         related_name='usuarios'
                     )
    cargo          = models.CharField(max_length=20, choices=CARGO_CHOICES,
                                      blank=True)
    departamento   = models.CharField(max_length=100, blank=True,
                                      help_text='Departamento de Bolivia donde trabaja')
    telefono       = models.CharField(max_length=20, blank=True)
    documento_identidad = models.CharField(max_length=20, blank=True,
                                           help_text='CI o carnet institucional')
    motivo_solicitud = models.TextField(blank=True,
                                        help_text='Por qué solicita acceso al sistema')
    aprobado_por   = models.ForeignKey(
                         'self',
                         on_delete=models.SET_NULL,
                         null=True, blank=True,
                         related_name='usuarios_aprobados'
                     )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    activo_sistema   = models.BooleanField(default=False,
                                           help_text='True cuando el admin aprueba la cuenta')

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    @property
    def es_superadmin(self):
        return self.rol == 'SUPERADMIN'

    @property
    def es_admin(self):
        return self.rol in ['SUPERADMIN', 'ADMIN_DSA']

    @property
    def puede_editar(self):
        return self.rol in ['SUPERADMIN', 'ADMIN_DSA', 'TECNICO']

    @property
    def solo_lectura(self):
        return self.rol in ['DOCENTE', 'ESTUDIANTE']

class SesionActiva(models.Model):
    """Rastrea usuarios actualmente en línea."""
    usuario      = models.OneToOneField(
                       Usuario, on_delete=models.CASCADE,
                       related_name='sesion_activa')
    ultimo_acceso = models.DateTimeField(auto_now=True)
    ip            = models.GenericIPAddressField(null=True, blank=True)
    navegador     = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Sesión Activa'

    def __str__(self):
        return f"{self.usuario.username} — {self.ultimo_acceso}"

    @property
    def esta_en_linea(self):
        from django.utils import timezone
        limite = timezone.now() - timezone.timedelta(minutes=10)
        return self.ultimo_acceso >= limite


class RegistroActividad(models.Model):
    """Auditoría de acciones realizadas en el sistema."""
    ACCION_CHOICES = [
        ('LOGIN',    'Inicio de sesión'),
        ('LOGOUT',   'Cierre de sesión'),
        ('VER',      'Ver registro'),
        ('CREAR',    'Crear registro'),
        ('EDITAR',   'Editar registro'),
        ('ELIMINAR', 'Eliminar registro'),
        ('EXPORTAR', 'Exportar datos'),
        ('OTRO',     'Otra acción'),
    ]

    usuario    = models.ForeignKey(
                     Usuario, on_delete=models.SET_NULL,
                     null=True, related_name='actividades')
    accion     = models.CharField(max_length=15, choices=ACCION_CHOICES)
    modulo     = models.CharField(max_length=100,
                     help_text='App o sección donde ocurrió la acción')
    descripcion = models.TextField(blank=True)
    ip          = models.GenericIPAddressField(null=True, blank=True)
    fecha       = models.DateTimeField(auto_now_add=True)
    objeto_id   = models.IntegerField(null=True, blank=True)
    objeto_repr = models.CharField(max_length=300, blank=True,
                     help_text='Representación del objeto afectado')

    class Meta:
        verbose_name        = 'Registro de Actividad'
        verbose_name_plural = 'Registros de Actividad'
        ordering            = ['-fecha']

    def __str__(self):
        return f"{self.usuario} — {self.get_accion_display()} — {self.modulo}"