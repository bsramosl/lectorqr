from django.shortcuts import render,redirect 
from PrincipalApp.models import *
from PrincipalApp.forms import *
from django.views.generic import TemplateView,ListView, CreateView, DeleteView, RedirectView,DetailView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import *
from django.db.models import CharField, Value as V

 

class UpdateVehiculo(UpdateView):
    template_name = 'Vehiculo/Update.html'    
    model = VehiculoModel
    form_class = VehiculoForm
    success_url = reverse_lazy('Qr:ListUser')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'Editar Vehiculo'
        context['list'] = 'Qr:ListUser' 
        return context 
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Vehiculo Actualizado con exito')
        return response