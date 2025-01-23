import re
from django import forms
from django.contrib.auth.models import User
from .models import Departamento, Residente, MovimientoDePago, Pago, Factura, Servicio, Mantenimiento, Edificio
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Solicitud

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Correo electrónico o usuario')
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')


class RegistroResidenteForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirmar contraseña')
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = Residente
        fields = ['user', 'documento_identidad', 'nacionalidad', 'telefono', 'departamento', 'email']
        widgets = {
            'user': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'documento_identidad': forms.TextInput(),
            'telefono': forms.TextInput(),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('usuario').password
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password_confirm

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('usuario').password
        # Verificar que la contraseña cumpla los requisitos
        if not re.match(r'^(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$', password):
            raise ValidationError("La contraseña debe tener al menos 8 caracteres, incluir un número y un carácter especial.")
        return cleaned_data

    def save(self, commit=True):
        # Crea el usuario con el correo electrónico
        user = User.objects.create_user(
            username=self.cleaned_data['user'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']  # Asignamos el correo del usuario aquí
        )

        # Crea el residente
        residente = Residente.objects.create(
            user=user,
            documento_identidad=self.cleaned_data['documento_identidad'],
            nacionalidad=self.cleaned_data['nacionalidad'],
            telefono=self.cleaned_data['telefono'],
            departamento=self.cleaned_data['departamento']
        )

        return residente
    
class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['numero', 'piso']
        widgets = {
            'numero': forms.TextInput(attrs={'maxlength': '50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['user', 'documento_identidad', 'nacionalidad', 'telefono', 'departamento']
        widgets = {
            'user': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'documento_identidad': forms.TextInput(),
            'telefono': forms.TextInput(),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        # Crea el residente
        residente = super().save(commit=False)
        if commit:
            residente.save()
        return residente
    
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo_pago', 'servicios']  # Asegúrate de incluir 'servicios'

    def save(self, commit=True):
        # Guarda el pago
        pago = super().save(commit=False)
        if commit:
            pago.save()
        
        # Agregar los servicios seleccionados al pago
        servicios = self.cleaned_data.get('servicios')
        if servicios:
            pago.servicios.set(servicios)  # Asociar los servicios seleccionados

        pago.calcular_total()  # Actualiza el monto total

        return pago
    
class MovimientoDePagoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso'),
    ]
    
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=True)
    
    class Meta:
        model = MovimientoDePago
        fields = ['pago', 'tipo', 'descripcion']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['fecha','monto_total', 'monto_pagado', 'descripcion', 'departamento','estado','usuario','pago']

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['descripcion']

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['fecha', 'descripcion', 'departamento']

class SolicitarMantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['descripcion']  # Asegúrate de tener estos campos en tu modelo

class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'departamento']


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo', 'descripcion']    

    titulo = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la solicitud'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción detallada'}))     

class NotificacionResidenteForm(forms.Form):
    residentes = forms.ModelMultipleChoiceField(
        queryset=Residente.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona a los residentes"
    )
    asunto = forms.CharField(max_length=100, label="Asunto")
    mensaje_base = forms.CharField(
        widget=forms.Textarea,
        label="Mensaje Base",
        help_text="Puedes usar {{ nombre }} y {{ deuda_pendiente }} para personalizar."
    )