
from PrincipalApp.models import *
from PrincipalApp.forms import *
from django.views.generic import TemplateView,ListView, CreateView, DeleteView, RedirectView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import *
from django.db.models import CharField, Value as V
from django.forms.models import inlineformset_factory



class ListUser(TemplateView):
    template_name = 'User/List.html'
 

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs) 
        context['create'] = 'Qr:CreateUser'
        context['update'] = 'Qr:UpdateUser' 
        context['delete'] = 'Qr:DeleteUser' 
        context['upd'] = 'Qr:UpdateVehiculo' 
        data=[]
        us = PersonaModel.objects.all()
        for i in us:
            item = i.toJSON()
            item['tipousuario'] = i.tipousuario
            vh= VehiculoModel.objects.filter(persona_id=i.id)
            for j in vh:                
                item['vehiculo_id'] = j.id 
                item['marca'] = j.modelo
                item['placa'] = j.placa 
            data.append(item)     
        context['object_list'] = data
        return context  


QuestionFormset = inlineformset_factory(
    PersonaModel, VehiculoModel,form=VehiculoForm, can_delete= False,max_num=1)


class CreateUser(CreateView):
    template_name = 'User/Create.html'
    model = PersonaModel
    form_class = RegistroFormulario
    success_url = reverse_lazy('Qr:ListUser')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Usuarios'
        context['list'] = 'Qr:ListUser' 
        if self.request.POST:
            context["question"] = QuestionFormset(self.request.POST)
        else:
            context["question"] = QuestionFormset() 
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        question = context["question"]
        self.object = form.save()
        if question.is_valid():
            question.instance = self.object
            question.save() 
        return super().form_valid(form)
 

class UpdateUser(UpdateView):
    template_name = 'User/Update.html'    
    model = PersonaModel
    form_class = RegistroFormulario
    success_url = reverse_lazy('Qr:ListUser')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Editar Usuario'
        context['list'] = 'Qr:ListUser' 
        return context 
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario Actualizado con exito')
        return response

class DeleteUser(DeleteView):
    template_name = 'User/Delete.html'
    model = User
    success_url = reverse_lazy('Qr:ListUser') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'User'
        context['delete'] = 'Qr:DeleteUser' 
        return context