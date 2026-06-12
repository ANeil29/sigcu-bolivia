from django import forms
from .models import Carrera, PlanEstudio


class CarreraForm(forms.ModelForm):
    class Meta:
        model  = Carrera
        fields = ['sede', 'nombre', 'programa', 'area', 'grado', 'tipo',
                  'diploma_academico', 'titulo_profesional',
                  'enfoque_curricular', 'en_funcionamiento',
                  'numero_sub', 'observaciones']
        widgets = {
            'sede':               forms.Select(attrs={'class': 'form-select'}),
            'nombre':             forms.TextInput(attrs={'class': 'form-control'}),
            'programa':           forms.TextInput(attrs={'class': 'form-control'}),
            'area':               forms.NumberInput(attrs={'class': 'form-control',
                                                            'min': 1, 'max': 5}),
            'grado':              forms.Select(attrs={'class': 'form-select'}),
            'tipo':               forms.Select(attrs={'class': 'form-select'}),
            'diploma_academico':  forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'enfoque_curricular': forms.Select(attrs={'class': 'form-select'}),
            'en_funcionamiento':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_sub':         forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'sede':               'Sede *',
            'nombre':             'Nombre de la Carrera *',
            'programa':           'Programa (si aplica)',
            'area':               'Área del conocimiento (1-6 SUB) *',
            'grado':              'Grado *',
            'tipo':               'Tipo *',
            'diploma_academico':  'Diploma académico',
            'titulo_profesional': 'Título profesional',
            'enfoque_curricular': 'Enfoque curricular',
            'en_funcionamiento':  '¿En funcionamiento?',
            'numero_sub':         'N° correlativo SUB',
            'observaciones':      'Observaciones',
        }


class PlanEstudioForm(forms.ModelForm):
    class Meta:
        model  = PlanEstudio
        fields = ['carrera', 'anio_aprobacion', 'evento_aprobacion',
                  'resolucion_hcu', 'resolucion_ran', 'activo']
        widgets = {
            'carrera':           forms.Select(attrs={'class': 'form-select'}),
            'anio_aprobacion':   forms.NumberInput(attrs={'class': 'form-control',
                                                           'min': 1970, 'max': 2100}),
            'evento_aprobacion': forms.TextInput(attrs={'class': 'form-control'}),
            'resolucion_hcu':    forms.TextInput(attrs={'class': 'form-control'}),
            'resolucion_ran':    forms.TextInput(attrs={'class': 'form-control'}),
            'activo':            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'carrera':           'Carrera *',
            'anio_aprobacion':   'Año de aprobación *',
            'evento_aprobacion': 'Evento de aprobación',
            'resolucion_hcu':    'Resolución HCU',
            'resolucion_ran':    'Resolución RAN',
            'activo':            '¿Plan activo?',
        }