from django.db import models  
from datetime import datetime 
from django.forms import model_to_dict 
from django.contrib.auth.models import User , AbstractUser
import random 


class TipoPersonaModel(models.Model):
    descripcion = models.CharField(max_length=250,default='Descripcion') 
    estado = models.CharField(max_length=12,default='Estado') 

    def __str__(self):
        return self.descripcion 

    def toJSON(self):
        item = model_to_dict(self)       
        return item    
      
    class Meta:
        verbose_name ='TipoPersona'
        verbose_name_plural = 'TipoPersonas'
        ordering = ['id']
        

class PersonaModel(AbstractUser):
    tipousuario = models.ForeignKey(TipoPersonaModel, related_name="TipoUsuario", on_delete=models.CASCADE,null=True,blank=True)       
    estado = models.CharField(max_length=8,default='Salida',null=True,blank=True) 
    cedula = models.IntegerField(verbose_name='Cedula',null=True,blank=True)

    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def toJSON(self):
        item = model_to_dict(self)       
        return item    
      
    class Meta:
        verbose_name ='Persona'
        verbose_name_plural = 'Persona'
        ordering = ['id']
     

class VehiculoModel(models.Model):
    persona = models.ForeignKey(PersonaModel, related_name="Persona", on_delete=models.CASCADE,null=True,blank=True)       
    color = models.CharField(max_length=8,default='Color',null=True,blank=True)
    modelo = models.CharField(max_length=20,default='Modelo',null=True,blank=True)
    placa = models.CharField(max_length=8,default='Placa',null=True,blank=True)
    estado = models.CharField(max_length=8,default='Estado',null=True,blank=True)

    def __str__(self):
        return self.modelo

    def toJSON(self):
        item = model_to_dict(self)       
        return item    
      
    class Meta:
        verbose_name ='Vehiculo'
        verbose_name_plural = 'Vehiculos'
        ordering = ['id']

class NovedadesModel(models.Model):
    observacion = models.CharField(max_length=250,default='Observacion',null=True,blank=True)
    estado = models.CharField(max_length=8,default='Estado',null=True,blank=True)

    def __str__(self):
        return self.observacion

    def toJSON(self):
        item = model_to_dict(self)       
        return item    
      
    class Meta:
        verbose_name ='Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['id']


class Registro(models.Model):
    persona = models.ForeignKey(PersonaModel, related_name="Usuario", on_delete=models.CASCADE)   
    novedades = models.ForeignKey(NovedadesModel, related_name="Novedades", on_delete=models.CASCADE,null=True,blank=True)       
    fecha_entrada = models.DateTimeField(auto_now_add=True,blank=True)
    fecha_salida = models.DateTimeField(null=True,blank=True)
    estado = models.CharField(max_length=8,  default='Salida')
    
    def __str__(self):
        return self.persona.first_name + ' ' + self.persona.last_name

    def toJSON(self):
        item = model_to_dict(self)       
        return item    

    class Meta: 
        verbose_name ='Registro'
        verbose_name_plural = 'Registros'
        ordering = ['id']