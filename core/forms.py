from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField

class ObraForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Obra
        fields = ['titulo', 'imagen', 'descripcion', 'historia', 'precio', 'tecnica', 'es_destacado']
        
class MsjObraForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Obra
        fields = ['mensaje']
        
class AObraForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Obra
        fields = ['titulo', 'descripcion', 'historia', 'precio', 'tecnica', 'es_destacado']

class TecnicaForm(ModelForm):
    class Meta:
        model = Tecnica
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class FiltroForm(forms.Form):
    tecnica = forms.ModelChoiceField(queryset=Tecnica.objects.all(), required=False)