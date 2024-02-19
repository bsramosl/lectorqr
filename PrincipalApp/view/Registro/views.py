from django.shortcuts import render,redirect 
from PrincipalApp.models import *
from PrincipalApp.forms import *
from django.views.generic import TemplateView,ListView, CreateView, DeleteView, RedirectView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import *
from django.db.models import CharField, Value as V

 

  
class ListRegistro(TemplateView):
    template_name = 'Registro/List.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['create'] = 'Qr:CreateObservacion' 
        context['update'] = 'Qr:MostRegistro' 
        context['delete'] = 'Qr:DeleteRegistro'        
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
    

class CreateSalida(UpdateView):
    template_name = 'Registro/CreateSalida.html'
    model = Registro
    form_class = NovedadesForm
    success_url = reverse_lazy('Qr:ListInvitado')
    
    def form_valid(self,form, *args, **kwargs):   
        response = super().form_valid(form) 
        reg = Registro.objects.filter(persona_id=self.object.persona.id).last()
        PersonaModel.objects.filter(id=self.object.persona.id).update(estado='Salida')
        if self.request.POST.get('observacion') != "":
            NovedadesModel.objects.create(observacion=self.request.POST.get('observacion'),estado='Salida')
            nov = NovedadesModel.objects.all().last()
            Registro.objects.filter(id=reg.id).update(estado='Salida',novedades_id=nov.id,fecha_salida=datetime.now())
        else:
            Registro.objects.filter(id=reg.id).update(estado='Salida',fecha_salida=datetime.now())           
        messages.success(self.request, 'Se ha registrado con exito')
        return response
        
def MostRegistro(request,id):
    data = []            
    per = PersonaModel.objects.filter(id=id)
    qs = Registro.objects.filter(persona_id=id)
    for i in qs:
        item = i.toJSON()
        print(i.fecha_entrada) 
        item['fecha_entrada'] = i.fecha_entrada
        item['vehiculo'] = VehiculoModel.objects.filter(persona_id = id).last()       
        item['persona'] = i.persona.first_name
        data.append(item)
    return render(request,"Registro/Update.html", 
                  context={'rec':data})

class DeleteRegistro(DeleteView):
    template_name = 'Registro/Delete.html'
    model = Registro
    success_url = reverse_lazy('Qr:ListRegistro') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Registro'
        context['delete'] = 'Qr:DeleteRegistro' 
        return context
    
