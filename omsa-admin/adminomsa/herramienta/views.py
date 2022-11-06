from django.shortcuts import render
from obra.models import Obra
from .models import Herramienta
from .forms import HerramientaForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy



class StaffRquiredMixin(object):
    """
    Este mixin requerira que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRquiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.

# ------------------------------------------------------------------------------------------ Herramienta List

class HerramientaListView(ListView):
    model = Herramienta

# ------------------------------------------------------------------------------------------ Herramienta Detail


class HerramientaUpdate(UpdateView):
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/update.html'

    def get_success_url(self):
        return reverse_lazy('herramienta:herramienta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['herramienta'] = self.model.objects.all()
        return context

# ------------------------------------------------------------------------------------------ Herramienta Create

class HerramientaCreate(CreateView):
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/create.html'

#    fields = ['title', 'content', 'order']
    success_url = reverse_lazy('herramienta:herramienta')