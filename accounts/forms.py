from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from universidades.models import Universidad


class FormularioRegistro(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Mínimo 8 caracteres'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Repite la contraseña'})
    )

    class Meta:
        model  = Usuario
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'cargo', 'departamento', 'telefono',
            'universidad', 'documento_identidad', 'motivo_solicitud',
        ]
        widgets = {
            'first_name':          forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':           forms.TextInput(attrs={'class': 'form-control'}),
            'username':            forms.TextInput(attrs={'class': 'form-control'}),
            'email':               forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo':               forms.Select(attrs={'class': 'form-select'}),
            'departamento':        forms.Select(attrs={'class': 'form-select'},
                                                choices=[
                                                    ('', '-- Selecciona --'),
                                                    ('Potosí',       'Potosí'),
                                                    ('La Paz',       'La Paz'),
                                                    ('Cochabamba',   'Cochabamba'),
                                                    ('Santa Cruz',   'Santa Cruz'),
                                                    ('Oruro',        'Oruro'),
                                                    ('Sucre',        'Sucre'),
                                                    ('Tarija',       'Tarija'),
                                                    ('Beni',         'Beni'),
                                                    ('Pando',        'Pando'),
                                                ]),
            'telefono':            forms.TextInput(attrs={'class': 'form-control'}),
            'universidad':         forms.Select(attrs={'class': 'form-select'}),
            'documento_identidad': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_solicitud':    forms.Textarea(attrs={'class': 'form-control',
                                                          'rows': 3}),
        }
        labels = {
            'first_name':          'Nombres',
            'last_name':           'Apellidos',
            'username':            'Nombre de usuario',
            'email':               'Correo electrónico',
            'cargo':               'Cargo o función',
            'departamento':        'Departamento',
            'telefono':            'Teléfono/Celular',
            'universidad':         'Universidad a la que pertenece',
            'documento_identidad': 'Número de CI o carnet',
            'motivo_solicitud':    '¿Por qué solicita acceso al sistema?',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.rol            = 'PENDIENTE'
        user.activo_sistema = False
        user.is_active      = False  
        if commit:
            user.save()
        return user


class FormularioAsignarRol(forms.ModelForm):
    """Formulario que usa el superadmin para aprobar y asignar rol."""
    class Meta:
        model  = Usuario
        fields = ['rol', 'universidad', 'cargo', 'departamento']
        widgets = {
            'rol':         forms.Select(attrs={'class': 'form-select'}),
            'universidad': forms.Select(attrs={'class': 'form-select'}),
            'cargo':       forms.Select(attrs={'class': 'form-select'}),
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
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'autofocus': True})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )