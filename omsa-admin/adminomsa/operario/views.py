from django.shortcuts import render
from obra.models import Montaje

from obra.models import Obra
from .models import Operario, Actividad, Presentismo, Dia
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import OperarioForm
import pandas as pd
from collections import defaultdict
from datetime import datetime, time
from django.shortcuts import get_object_or_404
from django.utils.encoding import uri_to_iri 
 

class StaffRquiredMixin(object):
    """
    Este mixin requerira que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRquiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.

# ------------------------------------------------------------------------------------------ Operario List

class OperarioListView(ListView):
    model = Operario

# ------------------------------------------------------------------------------------------ Operario Inactivo

class InactivoListView(ListView):
    model = Operario
    template_name = 'operario/operario_inactivo.html'

# ------------------------------------------------------------------------------------------ Operario Create



# ------------------------------------------------------------------------------------------ Operario Detail


class OperarioUpdate(UpdateView):
    model = Operario
    form_class = OperarioForm
    template_name = 'operario/update.html'

    def get_success_url(self):
        return reverse_lazy('operario:operario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operario'] = self.model.objects.all()
        return context

# ------------------------------------------------------------------------------------------ Operario Create

class OperarioCreate(CreateView):
    model = Operario
    form_class = OperarioForm
    template_name = 'operario/operario_create.html'

#    fields = ['title', 'content', 'order']
    success_url = reverse_lazy('operario:operario')


# ------------------------------------------------------------------------------------------ Fecha List calendario

class DiaListView(ListView):
    model = Dia
    
    def get_success_url(self):
        return reverse_lazy('operario:operario', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['presentismo'] = Presentismo.objects.all()
        context['actividad'] = Actividad.objects.all()
        context['obra'] = Obra.objects.all()
        context['dias'] = Dia.objects.all()

        prom_carga = []
        prom_pres = []


        for d in Dia.objects.all():
            pers_activo = Presentismo.objects.filter(fecha=d).count()
            present = Presentismo.objects.filter(fecha=d, estado="Presente").count()
            carga = Presentismo.objects.filter(fecha=d, cargado=True).count()
            if carga != 0:
                n = round(carga/pers_activo*100,2)
                prom_carga.append(n)
            else:
                prom_carga.append(0)

            if present != 0:
                n = round(present/pers_activo*100,2)
                prom_pres.append(n)
            else:
                prom_pres.append(0)
        
        prom = zip(Dia.objects.all(), prom_pres, prom_carga)
        context['prom'] = prom

        return context

    def dispatch(self, request, *args, **kwargs):
        dias = Dia.objects.values_list('fecha', flat=True).order_by('fecha')
        dias_list = pd.bdate_range(start=dias[0],end=datetime.today())
        dias_create = []
        for d in dias_list:
            if d.date() not in dias: #si aparece algun error, esta aca
                dias_create.append(d)
        for dc in dias_create:
            Dia.objects.create(fecha=dc, slug=dc.strftime("%y%m%d"))
        for p in Operario.objects.filter(estado="Activo"):
            for dcc in Dia.objects.all():
                if dcc.fecha in dias_create:
                    Presentismo.objects.create(
                        operario=p,
                        obra=p.obra_actual,
                        fecha=dcc,
                        hora_ingreso=time(7, 0),
                        hora_egreso=time(16, 0),
                        actividad_id=1
                    )
        return super().dispatch(request, *args, **kwargs)

# ------------------------------------------------------------------------------------------ Fecha Detail

class DiaUpdate(DetailView):
    model = Dia
    template_name = 'operario/dia_update.html'

    def get_success_url(self):
        return reverse_lazy('operario:fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['presentismo'] = Presentismo.objects.filter(fecha_id=self.object.id)
        context['actividad'] = Actividad.objects.all()
        context['obra'] = Obra.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            obra_hoy = dict(zip(request.POST.getlist('id'), request.POST.getlist('obra'))) 
            estado = dict(zip(request.POST.getlist('id'), request.POST.getlist('estado')))
            ingreso = dict(zip(request.POST.getlist('id'), request.POST.getlist('hora_ingreso')))
            egreso = dict(zip(request.POST.getlist('id'), request.POST.getlist('hora_egreso')))
            actividad = dict(zip(request.POST.getlist('id'), request.POST.getlist('actividad')))
            observaciones = dict(zip(request.POST.getlist('id'), request.POST.getlist('observaciones')))

            dd = defaultdict(list)
            for d in (obra_hoy, estado, ingreso, egreso, actividad, observaciones): 
                for key, value in d.items():
                    dd[key].append(value)
            
            for key, value in dd.items():
                e = Presentismo.objects.get(id=key)
                if value[0] != "x":
                    e.obra_id = value[0]
                e.estado = value[1]
                e.hora_ingreso = value[2]
                e.hora_egreso = value[3]
                e.actividad_id = value[4]
                if value[5] != "":
                    e.observaciones = value[5]
                e.save()

            id_cargado = request.POST.getlist('cargado')
            print(id_cargado)
            for x in id_cargado:
                Presentismo.objects.filter(id=int(x)).update(cargado=True) 


            return self.get(request, *args, **kwargs)

