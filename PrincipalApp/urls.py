from django.urls import path
from PrincipalApp import views 
from django.contrib.auth.decorators import login_required  
from PrincipalApp.view.Registro.views import *
from PrincipalApp.view.Persona.views import *
from PrincipalApp.view.Vehiculo.views import *



app_name = 'Qr'
urlpatterns = [  
     path('Index/',views.Index,name='Index'),    
     path('',login_required(views.Inicio.as_view()),name='Inicio'),       
     #path('Iniciolista/', login_required(views.Iniciolista.as_view()), name='Iniciolista'),  

     path('Dashboard/',login_required(views.Dashboard.as_view()),name='Dashboard'), 

     path('Login/', views.Login.as_view(), name='Login'),
	path('Logout/', views.Logout.as_view(), name='Logout'), 
    
     path('ListUser/',login_required(ListUser.as_view()),name='ListUser'),
     path('CreateUser/',CreateUser.as_view(),name='CreateUser'),
     path('UpdateUser/<int:pk>/',login_required(UpdateUser.as_view()),name='UpdateUser'),
     path('DeleteUser/<int:pk>/',login_required(DeleteUser.as_view()),name='DeleteUser'),

     
     path('UpdateVehiculo/<int:pk>/',login_required(UpdateVehiculo.as_view()),name='UpdateVehiculo'),

     path('ListRegistro/',login_required(ListRegistro.as_view()),name='ListRegistro'),
     
     path('CreateObservacion/<int:pk>/',login_required(views.CreateObservacion.as_view()),name='CreateObservacion'),

     path('ListInvitado/',login_required(views.ListInvitado.as_view()),name='ListInvitado'),
     path('CreateInvitado/',login_required(views.CreateInvitado.as_view()),name='CreateInvitado'),
     path('CreateIngreso/<int:pk>/',login_required(views.CreateIngreso.as_view()),name='CreateIngreso'),

     path('Informe/',login_required(views.Informe.as_view()),name='Informe'),
     path('busqueda/',login_required(views.busqueda),name='busqueda'),

     path('Email/',login_required(views.Email),name='Email'),

     path('CreateSalida/<int:pk>/',login_required(CreateSalida.as_view()),name='CreateSalida'),
     path('MostRegistro/<int:id>/',login_required(MostRegistro),name='MostRegistro'),
     path('DeleteRegistro/<int:pk>/',login_required(DeleteRegistro.as_view()),name='DeleteRegistro'),
    ]