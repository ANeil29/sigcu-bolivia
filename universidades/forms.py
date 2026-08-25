from django import forms
from .models import Universidad, Facultad, Sede


class UniversidadForm(forms.ModelForm):
    class Meta:
        model  = Universidad
        fields = ['nombre', 'sigla', 'departamento', 'rector',
                  'telefono', 'website', 'activa']
        widgets = {
            'nombre':       forms.TextInput(attrs={'class': 'form-control'}),
            'sigla':        forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-select'},
                                         choices=[
                                             ('', '-- Selecciona --'),
                                             ('Potosí',     'Potosí'),
                                             ('La Paz',     'La Paz'),
                                             ('Cochabamba', 'Cochabamba'),
                                             ('Santa Cruz', 'Santa Cruz'),
                                             ('Oruro',      'Oruro'),
                                             ('Sucre',      'Sucre'),
                                             ('Tarija',     'Tarija'),
                                             ('Beni',       'Beni'),
                                             ('Pando',      'Pando'),
                                         ]),
            'rector':       forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':     forms.TextInput(attrs={'class': 'form-control'}),
            'website':      forms.URLInput(attrs={'class': 'form-control'}),
            'activa':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre':       'Nombre completo',
            'sigla':        'Sigla (ej: UATF)',
            'departamento': 'Departamento',
            'rector':       'Rector actual',
            'telefono':     'Teléfono',
            'website':      'Sitio web',
            'activa':       '¿Activa?',
        }


class FacultadForm(forms.ModelForm):
    class Meta:
        model  = Facultad
        fields = ['universidad', 'nombre', 'sigla', 'decano', 'telefono']
        widgets = {
            'universidad': forms.Select(attrs={'class': 'form-select'}),
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'sigla':       forms.TextInput(attrs={'class': 'form-control'}),
            'decano':      forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':    forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'universidad': 'Universidad',
            'nombre':      'Nombre de la Facultad',
            'sigla':       'Sigla',
            'decano':      'Decano actual',
            'telefono':    'Teléfono',
        }


class SedeForm(forms.ModelForm):
    class Meta:
        model  = Sede
        fields = ['facultad', 'nombre', 'tipo', 'departamento', 'ciudad',
                  'direccion', 'telefono', 'latitud', 'longitud',
                  'imagen_referencia', 'descripcion', 'activa']
        widgets = {
            'facultad':    forms.Select(attrs={'class': 'form-select'}),
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'tipo':        forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'},
                                          choices=[
                                              ('', '-- Selecciona --'),
                                              ('Potosí',     'Potosí'),
                                              ('La Paz',     'La Paz'),
                                              ('Cochabamba', 'Cochabamba'),
                                              ('Santa Cruz', 'Santa Cruz'),
                                              ('Oruro',      'Oruro'),
                                              ('Sucre',      'Sucre'),
                                              ('Tarija',     'Tarija'),
                                              ('Beni',       'Beni'),
                                              ('Pando',      'Pando'),
                                          ]),
            'ciudad':      forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':   forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 2}),
            'telefono':    forms.TextInput(attrs={'class': 'form-control'}),
            'latitud':     forms.NumberInput(attrs={'class': 'form-control',
                                                     'step': 'any',
                                                     'placeholder': 'Ej: -19.5836'}),
            'longitud':    forms.NumberInput(attrs={'class': 'form-control',
                                                     'step': 'any',
                                                     'placeholder': 'Ej: -65.7531'}),
            'imagen_referencia': forms.FileInput(attrs={'class': 'form-control',
                                                         'accept': 'image/*'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 3}),
            'activa':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'facultad':    'Facultad *',
            'nombre':      'Nombre de la Sede *',
            'tipo':        'Tipo *',
            'departamento': 'Departamento *',
            'ciudad':      'Ciudad *',
            'direccion':   'Dirección',
            'telefono':    'Teléfono',
            'latitud':     'Latitud (coordenada Y)',
            'longitud':    'Longitud (coordenada X)',
            'imagen_referencia': 'Imagen de referencia',
            'descripcion': 'Descripción de la sede',
            'activa':      '¿Activa?',
        }