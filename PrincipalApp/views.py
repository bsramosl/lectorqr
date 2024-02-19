from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect 
from .models import *
from .forms import * 
from django.http import StreamingHttpResponse
import cv2
import threading
from django.views.generic import TemplateView,ListView, CreateView, DeleteView, RedirectView,DetailView,UpdateView
import time
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash,authenticate
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView
from django.core.exceptions import *
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from datetime import datetime, timedelta
import json
from django.core.mail import send_mail
from django.db.models import Sum
from collections import Counter
from django.forms.models import inlineformset_factory

 

class Inicio(TemplateView):
    template_name = "Index.html" #nombre de plantilla html

    def get_context_data(self, **kwargs): #datos variables que se envian al template
        context = super().get_context_data(**kwargs)
        data = []#arreglo
        ct = PersonaModel.objects.all() #invocacion de todos los usuarios
        for i in ct: #recorrido de todos los usuarios
            if Registro.objects.filter(persona_id=i.id).exists():#pregunta si el registro de ese usuario existe 
                res = i.toJSON()#serializa objetos
                res["fecha"] = Registro.objects.filter(persona_id = i.id).latest('fecha_entrada')#obtine el ultimo registro por fecha
                data.append(res) #agrega datos al arreglo
            else:                
                pass
        context['persona'] = data #envia los datos al template
        return context

    def dato(con):#con es la informacion del qr
        print(f'Dato:{con}')#muestra informacion del qr
        author =  User.objects.annotate(screen_name=Concat('first_name', V(' ') ,'last_name')) # obtine el nombre de usuario y apellido
        for i in author: # recorre cada nombre de usuario
          if i.screen_name == con : # pregiunta si el nombre de usuario es igual dal dato leido por el qr
              user = PersonaModel.objects.get(id=i.id)#obtiene a la persona leida
              if user.tipousuario != "Invitado":#pregunta por el estado de la persona 
                 if user.estado == "Salida":
                     PersonaModel.objects.filter(id=i.id).update(estado='Entrada')#cambia el estado de la persona
                     Registro.objects.create(persona_id=i.id,estado='Entrada')#crea un nuevo resgistro
                     ul = Registro.objects.filter(persona_id=i.id).last()#obtine el ultimo registro de ese usuario
                     Registro.objects.filter(id = ul.id).update(fecha_entrada=datetime.now())
                 else:
                     PersonaModel.objects.filter(id=i.id).update(estado='Salida')#cambia el estado de la persona
                     ul = Registro.objects.filter(persona_id=i.id).last()#obtine el ultimo registro de ese usuario
                     Registro.objects.filter(id = ul.id).update(fecha_salida=datetime.now(),estado='Salida')      #cambia el estado en el registro         
        time.sleep(2) #espera 2 segundo pra leer mas registros por qr

class Dashboard(TemplateView):
    template_name = 'Dashboard.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['tuser'] = PersonaModel.objects.filter(estado = 'Entrada').count() #presenta cantidad de usuarios ingresados         
        data = []
        ct = PersonaModel.objects.filter(estado = 'Entrada')[:5]#ultimos 5 usuarios ingresados
        for i in ct:#recorre los usuarios
            res = i.toJSON()#agrega los datos de cada usuario
            data.append(res)           
        context['userc'] = data#datos de los 5 usuarios ingresados 
        context['fecha'] = User.objects.filter(last_login__isnull=False)  
        context['dia'] = Registro.objects.filter(fecha_entrada = datetime.now()).count()#registro de usuarios ingresados el dia de hoy
        total = PersonaModel.objects.all().count()#total de usuarios
        ingreso = PersonaModel.objects.filter(estado='Entrada').count()#total de usuarios ingresados en la institucion
        context['ingreso'] = ingreso
        if PersonaModel.objects.filter(estado='Entrada').filter(tipousuario = 2).exists():#pregunta si existen visitantes registrados
            context['visitante'] = PersonaModel.objects.filter(estado='Entrada').filter(tipousuario = 2).count() #cuenta visistantes engresados
        else:
              context['visitante'] = "Sin Datos"        
        salida = PersonaModel.objects.filter(estado='Salida').count()
        context['sal'] = salida#cantidadd de personas ausentes
        ingreso = round((ingreso * 100)/total,2)#porssentaje de personas ingresada
        salida = round((salida * 100)/total,2)#porsentaje de personas ausentes
        context['entrada'] = ingreso
        context['salida'] = salida
        #proceso para crear grafica  
        reg = Registro.objects.filter(fecha_entrada__month=datetime.now().month)   #pregunta por cntidad de registros ingresados por mes 
        lista=[]
        lis=[]
        cont_repe = 0 
        for i in reg:#precorre los registros por mes
            res = i.toJSON()
            dat = i.fecha_entrada.day
            for j in reg:
                re = j.toJSON()
                if j.fecha_entrada.day == dat:
                    if j.fecha_entrada.day not in lis:
                        cont_repe += 1 
            lis.append(dat)
            if cont_repe != 0:
                lista.append({'dia': i.fecha_entrada.strftime('%d-%m-%Y'),'dat' : cont_repe})
            cont_repe = 0
        context['tabla'] = lista           
        return context  
     


def Index(request):   
     cam = VideoCamera()     
     return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame") 
    

class VideoCamera(object):
    def __init__(self):#inicializa el objeto -- constructor
        self.video = cv2.VideoCapture(0)#inicializa la cual permitirá iniciar el proceso de captura del video.
        (self.grabbed, self.frame) = self.video.read()# desempaqueta dos valores, frame se almacenara captura de video
        threading.Thread(target=self.update, args=()).start()#comienza la captura del video

    def __del__(self): 
        self.video.release()

    def get_frame(self):
        qrdetector = cv2.QRCodeDetector()#iniciamos la lectura del qr
        data, bbox, rectifiedImage = qrdetector.detectAndDecode(self.frame)#data informacion del qr -  rectifiedImage es la foto del qr
        if len(data)>0:#preguntamos si existe alguna informacion en la lectura del qr         
             Inicio.dato(data)#envia la informacion del qr para realizar los procesos
        image = self.frame #guarda la captura del macro del video
        _, jpeg = cv2.imencode('.jpg', image)#transforma el video cuadro por cuadro a imagen jpg 
        return jpeg.tobytes()#transforma imagen a 2 bits 

    def update(self):#lee imagen por imagen y crea el video
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()  #obtiene el video creado y lo pasa para mostrar en el template html      
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        


 
class Login(FormView):
    template_name = 'Login.html'
    form_class = UsuarioLoginForm
    success_url = reverse_lazy('Qr:Inicio')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):#si es valido el ingreso de usuario
        login(self.request, form.get_user())
        messages.success(self.request, 'Bienvenido')
        return super(Login, self).form_valid(form)

    def form_invalid(self, form):#si es invalido el ingreso de usuario muestra los errores
        messages.error(self.request, form.errors)
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))  
    
class Logout(RedirectView):
    pattern_name = 'Qr:Login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)  
 


class ListInvitado(TemplateView):
    template_name = 'Invitado/List.html' 
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['creates'] = 'Qr:CreateInvitado'
        context['create'] = 'Qr:CreateObservacion'
        context['salida'] = 'Qr:CreateSalida'
        context['update'] = 'Qr:MostRegistro'
        context['entrada'] = 'Qr:CreateIngreso'
        data = []
        ct = PersonaModel.objects.all()               
        for i in ct:      
            res = i.toJSON()
            if Registro.objects.filter(persona_id=i.id).exists(): 
                re = Registro.objects.filter(persona_id=i.id).latest('fecha_entrada')
                reg = Registro.objects.filter(id=re.id)
                for j in reg:
                    res["fecha_entrada"] = j.fecha_entrada 
                    res["fecha_salida"] = j.fecha_salida  
                    nov = NovedadesModel.objects.filter(id=j.novedades_id)  
                    for k in nov:
                        res["observacion"] = k.observacion                        
                ve = VehiculoModel.objects.filter(persona_id=i.id)
                for m in ve:  
                    res["placa"] = m.placa
                    res["marca"] = m.modelo  
                tip=TipoPersonaModel.objects.filter(id=i.tipousuario_id)
                for l in tip:
                    res["tip"]= l.descripcion
            t = Registro.objects.filter(persona_id = i.id).latest('fecha_entrada')
            res["ultimo"] = t  
            data.append(res)   
        context['reg'] = data           
        return context 
    


QuestionFormset = inlineformset_factory(
    PersonaModel, VehiculoModel,form=VehiculoForm, can_delete= False,max_num=1)


class CreateInvitado(CreateView):
    template_name = 'Invitado/Create.html'    
    model = Registro
    form_class = RegistroFormulario
    success_url = reverse_lazy('Qr:ListInvitado')

    def form_valid(self,form, *args, **kwargs):    
        response = super().form_valid(form)
        pe = PersonaModel.objects.all().last().id
        PersonaModel.objects.filter(id=pe).update(estado="Entrada",tipousuario_id=self.request.POST.get('tipo'))
        Registro.objects.create(persona_id=pe,estado='Entrada')
        VehiculoModel.objects.create(color=self.request.POST.get('Persona-0-color'),modelo=self.request.POST.get('Persona-0-modelo'),
                                     placa=self.request.POST.get('Persona-0-placa'),estado=self.request.POST.get('Persona-0-estado')
                                     ,persona_id=pe)      
        messages.success(self.request, 'Se ha registrado con exito')
        return response 
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = 'Qr:ListInvitado'
        if self.request.POST:
            context["question"] = QuestionFormset(self.request.POST)
        else:
            context["question"] = QuestionFormset() 
        return context 


class CreateIngreso(UpdateView):
    template_name = 'Invitado/Ingreso.html'    
    model = Registro
    form_class = NovedadesForm
    success_url = reverse_lazy('Qr:ListInvitado')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = 'Qr:ListInvitado' 
        return context  
    
    def form_valid(self,form, *args, **kwargs):          
        response = super().form_valid(form) 
        if self.request.POST.get('observacion') != "":
            PersonaModel.objects.filter(id=self.object.persona.id).update(estado="Entrada")
            NovedadesModel.objects.create(observacion=self.request.POST.get('observacion'),estado="Entrada")
            nov = NovedadesModel.objects.all().last()
            Registro.objects.create(estado="Entrada",persona_id=self.object.persona.id,novedades_id=nov.id)
            NovedadesModel.objects.create(observacion=self.request.POST.get('observacion'),estado="Entrada")
        else:
            Registro.objects.create(estado="Entrada",persona_id=self.object.persona.id) 
            PersonaModel.objects.filter(id=self.object.persona.id).update(estado="Entrada")
        messages.success(self.request, 'Se ha registrado con exito')
        return response 

class CreateObservacion(UpdateView):
    template_name = 'Registro/Create.html'    
    model = Registro
    form_class = NovedadesForm
    success_url = reverse_lazy('Qr:ListRegistro')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = 'Qr:ListRegistro' 
        return context  
    
    def form_valid(self,form, *args, **kwargs):          
        response = super().form_valid(form)
        NovedadesModel.objects.create(observacion=self.request.POST.get('observacion'),estado=self.request.POST.get('estado'))
        nov = NovedadesModel.objects.all().last()
        ultimo = Registro.objects.filter(id=self.get_object().id).latest('fecha_entrada')

        Registro.objects.filter(id=ultimo.id).update(novedades=nov.id)
        messages.success(self.request, 'Se ha registrado con exito')
        return response 
    


class Informe(TemplateView):
    template_name = 'Consulta/Informe.html'

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def busqueda(request):
    data=[]    
    if is_ajax(request=request):    
        queryset = request.GET.get('nombre')        
        actio = request.GET.get('action') 
        if actio == 'busc':                
            if queryset != 0:          
                qs = Registro.objects.filter(fecha_entrada__date=queryset)                
                for i in qs:
                    res = i.toJSON() 
                    res['fecha_entrada']  = i.fecha_entrada.strftime("%m/%d/%Y, %H:%M:%S")
                    if i.fecha_salida != None:
                        res['fecha_salida']  = i.fecha_salida.strftime("%m/%d/%Y, %H:%M:%S")
                    else:
                        res['fecha_salida']  = "El Usuario se encuentra en la institucion"
                    nv = NovedadesModel.objects.filter(id=i.novedades_id)
                    for k in nv:
                        res['novedades'] = k.observacion
                    us = User.objects.filter(id=i.persona_id)
                    for j in us:
                        res['persona'] = j.first_name + ' ' + j.last_name    
                        tp=TipoPersonaModel.objects.filter(id=j.tipousuario_id)
                        for k in tp:
                            res['tipousuario'] = k.descripcion     
                    data.append(res) 
        return HttpResponse(json.dumps(list(data)), content_type='application/json')
    else:
        return HttpResponse("Solo Ajax")

from django.core.mail import EmailMessage

def Email(request):
    # CONTACT FORM
    
    if request.method == 'POST':
            name = request.POST.get('name')#nombre de persona que envia el email
            email = request.POST.get('email')#correo
            message = request.POST.get('message')#mensaje del email
            if request.POST.get('pdf') != "":
                pdf =  request.FILES['pdf']
                form_data = {
                'name':name,
                'email':email,
                'message':message,
                'pdf':pdf,
                }  
            else:
                 form_data = {
                'name':name,
                'email':email,
                'message':message,
                }                      
            email = EmailMessage('Informe Garita', message, '', [form_data['email']])   
            if request.FILES:
                uploaded_file = request.FILES
                for file in uploaded_file.getlist('pdf'):
                   email.attach(file.name, file.read(), file.content_type)  
                              
            email.send()
            messages.success(request, 'Mensaje Enviado con exito')
                       
    return render(request, 'Consulta/Email.html', {})