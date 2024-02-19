from builtins import property
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, Form, Select
from .models import *
from django.forms import DateInput, ModelForm, ModelChoiceField, Form, Select, TextInput 
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre de Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'}))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

class RegistroForm(ModelForm):
    
    class Meta:	
        model = Registro
        fields = ('__all__')

 

class Reg(UserCreationForm): 
     
    class Meta:
        model=User
        fields = '__all__'



class RegistroFormulario(ModelForm):
    username = forms.CharField(label="Nombre de Usuario",required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre",required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido",required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    cedula = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.ModelChoiceField(label="Tipo de Usuario",queryset=TipoPersonaModel.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-select input-height'}))

    class Meta:
        model=User 
        fields = [            
           'first_name',
           'last_name',
           'username',
           'email',
           'cedula', 
           'tipo',           
           ]

        

class VehiculoForm(ModelForm):
    color =  forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    modelo = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    placa = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:	
        model = VehiculoModel
        fields = ('__all__')


class NovedadesForm(ModelForm):
    observacion =  forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'})) 
    
    class Meta:	
        model = NovedadesModel
        fields = [ 
           'observacion',    
           ]