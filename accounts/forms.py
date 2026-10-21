from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from universidades.models import Universidad
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

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
    # ── Campo extra para cargo personalizado ──────────────────────────
    otro_cargo = forms.CharField(
        label='Especifica tu cargo',
        required=False,
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'placeholder': 'Escribe tu cargo o función...',
            'id':          'id_otro_cargo',
        })
    )

    class Meta:
        model  = Usuario
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'cargo', 'departamento', 'telefono',
            'universidad', 'documento_identidad', 'motivo_solicitud',
        ]
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'username':     forms.TextInput(attrs={'class': 'form-control'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo':        forms.Select(attrs={
                                'class':    'form-select',
                                'id':       'id_cargo',
                                'onchange': 'toggleOtroCargo(this)',
                            }),
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

    def clean(self):
        cleaned = super().clean()
        cargo = cleaned.get('cargo')
        otro  = cleaned.get('otro_cargo', '').strip()
        if cargo == 'OTRO' and not otro:
            self.add_error('otro_cargo',
                'Por favor especifica tu cargo cuando seleccionas "Otro".')
        return cleaned

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('Mínimo 8 caracteres.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # Si eligió "Otro" guarda el texto personalizado en observaciones
        if self.cleaned_data.get('cargo') == 'OTRO':
            otro = self.cleaned_data.get('otro_cargo', '').strip()
            if otro:
                user.cargo = 'OTRO'
                # Guarda el cargo personalizado en motivo_solicitud como referencia
                user.motivo_solicitud = (
                    f"[Cargo: {otro}]\n{self.cleaned_data.get('motivo_solicitud','')}"
                )
        user.rol            = 'PENDIENTE'
        user.activo_sistema = False
        user.is_active      = False
        if commit:
            user.save()
        return user


class FormularioAsignarRol(forms.ModelForm):
    otro_cargo = forms.CharField(
        label='Especifica el cargo',
        required=False,
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'placeholder': 'Escribe el cargo o función...',
            'id':          'id_otro_cargo_admin',
        })
    )

    class Meta:
        model  = Usuario
        fields = ['rol', 'cargo', 'departamento',
                  'universidad', 'activo_sistema']
        widgets = {
            'rol':           forms.Select(attrs={'class': 'form-select'}),
            'cargo':         forms.Select(attrs={
                                 'class':    'form-select',
                                 'id':       'id_cargo_admin',
                                 'onchange': 'toggleOtroCargoAdmin(this)',
                             }),
            'departamento':  forms.Select(attrs={'class': 'form-select'},
                                           choices=[
                                               ('','-- Selecciona --'),
                                               ('Potosí','Potosí'),
                                               ('La Paz','La Paz'),
                                               ('Cochabamba','Cochabamba'),
                                               ('Santa Cruz','Santa Cruz'),
                                               ('Oruro','Oruro'),
                                               ('Sucre','Sucre'),
                                               ('Tarija','Tarija'),
                                               ('Beni','Beni'),
                                               ('Pando','Pando'),
                                           ]),
            'universidad':   forms.Select(attrs={'class': 'form-select'}),
            'activo_sistema': forms.CheckboxInput(
                                  attrs={'class': 'form-check-input'}),
        }
        labels = {
            'rol':           'Rol en el sistema *',
            'cargo':         'Cargo o función',
            'departamento':  'Departamento',
            'universidad':   'Universidad',
            'activo_sistema': '¿Activo en el sistema?',
        }

    def clean(self):
        cleaned = super().clean()
        cargo = cleaned.get('cargo')
        otro  = cleaned.get('otro_cargo', '').strip()
        if cargo == 'OTRO' and not otro:
            self.add_error('otro_cargo',
                'Debes especificar el cargo cuando seleccionas "Otro".')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('cargo') == 'OTRO':
            otro = self.cleaned_data.get('otro_cargo', '').strip()
            if otro:
                # Guarda el cargo personalizado en observaciones del usuario
                user.observaciones = f"Cargo: {otro}"
        if commit:
            user.save()
        return user

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

class RecuperarContrasenaForm(PasswordResetForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el correo con el que te registraste'
        })
    )


class NuevaContrasenaForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Mínimo 8 caracteres.'
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CambiarContrasenaAdminForm(forms.Form):
    """Formulario para que el Superadmin restablezca la contraseña de un usuario."""
    nueva_contrasena = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    confirmar_contrasena = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('nueva_contrasena')
        p2 = cleaned_data.get('confirmar_contrasena')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data