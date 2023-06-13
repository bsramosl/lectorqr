from django.urls import path
from PrincipalApp import views 
from django.contrib.auth.decorators import login_required  



app_name = 'Qr'
urlpatterns = [  
     path('Index/',views.Index,name='Inicio'),    
     path('Inicio/',views.Inicio.as_view(),name='Inicio'),    
   
    ]