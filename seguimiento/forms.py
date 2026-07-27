from django import forms
from .models import TipoFase, ProcesoCurricular, FaseProceso


class TipoFaseForm(forms.ModelForm):
    class Meta:
        model  = TipoFase
        fields = ['codigo', 'nombre', 'descripcion',
                  'medio_verificacion_default', 'orden', 'activa']
        widgets = {
            'codigo':      forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Ej: F1'}),
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'medio_verificacion_default': forms.Textarea(attrs={'class': 'form-control',
                                                                 'rows': 2}),
            'orden':  forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'codigo':      'Código *',
            'nombre':      'Nombre de la fase *',
            'descripcion': 'Descripción',
            'medio_verificacion_default': 'Medio de verificación por defecto',
            'orden':  'Orden de aparición',
            'activa': '¿Activa?',
        }


class ProcesoCurricularForm(forms.ModelForm):
    class Meta:
        model  = ProcesoCurricular
        fields = ['carrera', 'tipo_proceso', 'nombre_proceso',
                  'anio_inicio', 'anio_conclusion', 'estado', 'observaciones']
        widgets = {
            'carrera':       forms.Select(attrs={'class': 'form-select'}),
            'tipo_proceso':  forms.Select(attrs={'class': 'form-select'}),
            'nombre_proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'anio_inicio':   forms.NumberInput(attrs={'class': 'form-control',
                                                       'min': 1990, 'max': 2100}),
            'anio_conclusion': forms.NumberInput(attrs={'class': 'form-control',
                                                         'min': 1990, 'max': 2100}),
            'estado':        forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'carrera':         'Carrera *',
            'tipo_proceso':    'Tipo de proceso *',
            'nombre_proceso':  'Nombre del proceso (opcional)',
            'anio_inicio':     'Año de inicio *',
            'anio_conclusion': 'Año de conclusión',
            'estado':          'Estado *',
            'observaciones':   'Observaciones',
        }


class FaseProcesoForm(forms.ModelForm):
    class Meta:
        model  = FaseProceso
        fields = ['proceso', 'tipo_fase', 'fecha_inicio', 'fecha_conclusion',
                  'medio_verificacion', 'estado', 'observaciones',
                  'archivo_verificacion']        # ← agrega este campo
        widgets = {
            'proceso':    forms.Select(attrs={'class': 'form-select'}),
            'tipo_fase':  forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control',
                                                    'type': 'date'}),
            'fecha_conclusion': forms.DateInput(attrs={'class': 'form-control',
                                                        'type': 'date'}),
            'medio_verificacion': forms.Textarea(attrs={'class': 'form-control',
                                                         'rows': 2}),
            'estado':       forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control',
                                                    'rows': 2}),
            'archivo_verificacion': forms.FileInput(
                attrs={'class': 'form-control',
                       'accept': '.pdf,.doc,.docx,.xls,.xlsx,.odt,.ods'}
            ),
        }
        labels = {
            'proceso':    'Proceso curricular *',
            'tipo_fase':  'Tipo de fase *',
            'fecha_inicio':    'Fecha de inicio',
            'fecha_conclusion': 'Fecha de conclusión',
            'medio_verificacion': 'Medio de verificación',
            'estado':       'Estado *',
            'observaciones': 'Observaciones',
            'archivo_verificacion': 'Documento de verificación',
        }