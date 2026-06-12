from django import forms
from .models import FormularioValoracion


class FormularioValoracionForm(forms.ModelForm):
    class Meta:
        model  = FormularioValoracion
        fields = ['proceso', 'codigo', 'fecha_elaboracion', 'responsable',
                  'estado', 'observaciones', 'archivo_adjunto']
        widgets = {
            'proceso':          forms.Select(attrs={'class': 'form-select'}),
            'codigo':           forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Ej: FV-2024-001'}),
            'fecha_elaboracion': forms.DateInput(attrs={'class': 'form-control',
                                                         'type': 'date'}),
            'responsable':      forms.TextInput(attrs={'class': 'form-control'}),
            'estado':           forms.Select(attrs={'class': 'form-select'}),
            'observaciones':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'archivo_adjunto':  forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'proceso':          'Proceso Curricular *',
            'codigo':           'Código del formulario *',
            'fecha_elaboracion': 'Fecha de elaboración *',
            'responsable':      'Responsable',
            'estado':           'Estado *',
            'observaciones':    'Observaciones',
            'archivo_adjunto':  'Archivo adjunto (PDF, Word)',
        }