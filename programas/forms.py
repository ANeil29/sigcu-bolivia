
from django import forms
from .models import Programa


DEPARTAMENTOS = [
    ('', '-- Selecciona --'),
    ('Potosí', 'Potosí'),
    ('La Paz', 'La Paz'),
    ('Cochabamba', 'Cochabamba'),
    ('Santa Cruz', 'Santa Cruz'),
    ('Oruro', 'Oruro'),
    ('Sucre', 'Sucre'),
    ('Tarija', 'Tarija'),
    ('Beni', 'Beni'),
    ('Pando', 'Pando'),
]


class ProgramaForm(forms.ModelForm):

    class Meta:
        model = Programa
        fields = [
            'sede', 'nombre', 'descripcion', 'area', 'grado_previsto',
            'estado', 'fecha_inicio', 'fecha_prevista_aprobacion',
            'resolucion_hcu', 'resolucion_ran', 'numero_sub',
            'responsable', 'observaciones', 'activo'
        ]

        widgets = {
            'sede': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1, 'max': 6
            }),
            'grado_previsto': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'fecha_prevista_aprobacion': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'resolucion_hcu': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'resolucion_ran': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'numero_sub': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'sede': 'Facultad y Sede *',
            'nombre': 'Nombre del Programa *',
            'descripcion': 'Descripción',
            'area': 'Área del conocimiento (1-6 SUB) *',
            'grado_previsto': 'Grado al que aspira',
            'estado': 'Estado actual *',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_prevista_aprobacion':
                'Fecha prevista de aprobación como carrera',
            'resolucion_hcu': 'Resolución HCU',
            'resolucion_ran': 'Resolución RAN',
            'numero_sub': 'N° SUB (si tiene)',
            'responsable': 'Responsable del programa',
            'observaciones': 'Observaciones',
            'activo': '¿Activo?',
        }

    # Este método debe estar dentro de ProgramaForm,
    # al mismo nivel que class Meta.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from universidades.models import Sede

        campo_sede = self.fields['sede']

        campo_sede.queryset = (
            Sede.objects
            .select_related('facultad')
            .filter(activa=True)
            .order_by('facultad__nombre', 'ciudad', 'nombre')
        )

        campo_sede.empty_label = '— Selecciona Facultad y Sede —'

        campo_sede.label_from_instance = (
            lambda sede: f"{sede.facultad.nombre} — {sede.nombre}"
        )
