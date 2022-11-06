from .models import Obra, Modulo, Montaje
from operario.models import Operario
from .forms import MontajeForm, ObraForm
from django.views.generic import ListView, DetailView, UpdateView, View, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import date, timedelta
import xlwt
from django.db.models import Sum
from django.http import JsonResponse
from collections import Counter
import pandas as pd  
from django.http import HttpResponseRedirect

class StaffRquiredMixin(object):
    """
    Este mixin requerira que el usuario sea miembro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRquiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.

# ------------------------------------------------------------------------------------------ Obra List

class ObraListView(ListView):
    model = Obra

# ------------------------------------------------------------------------------------------ Obra Create

class ObraCreate(CreateView):
    model = Obra
    form_class = ObraForm
    template_name = 'obra/obra_create.html'

#    fields = ['title', 'content', 'order']
    success_url = reverse_lazy('obra:obra')

    def form_valid(self, form):
        self.object = form.save()
        niveles = list(range(1, self.object.pisos + 1))
        print(niveles)
        posiciones = list(range(1, self.object.posiciones + 1))
        print(posiciones)
        Modulo.objects.create(
                    obra_id=self.object.id,
                    modulo='BASE'
                )
        mod = Modulo.objects.get(obra_id=self.object.id, modulo='BASE')
        print(mod)
        for n in niveles:
            for p in posiciones:
                Montaje.objects.create(
                    piso=n,
                    posicion=p,
                    modulo_id=mod.id
                )
        return HttpResponseRedirect(self.get_success_url())

# ------------------------------------------------------------------------------------------ Obra Update

class ObraUpdate(UpdateView):
    model = Obra
    form_class = ObraForm
    template_name = 'obra/obra_update.html'

    def get_success_url(self):
        return reverse_lazy('obra:detail', args=[self.object.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obra'] = self.model.objects.all()
        return context

    def form_valid(self, form):
        if form.has_changed():
            self.object.slug = self.object.obra_id
            self.object.save()
        return super().form_valid(form)

# ------------------------------------------------------------------------------------------ Obra Detail

class ObraDetailView(DetailView):
    model = Obra
    template_name = 'obra/obra_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = Montaje.objects.filter(modulo__obra=self.get_object())

        charts_data = Montaje.objects.filter(modulo__obra=self.get_object())
        total_mod = len([p for p in charts_data if p.modulo_id > 1])
        montado_mod = len([p for p in charts_data if p.identificador != None])
        completo_mod = 0
        for e in charts_data:
            if e.anclajes == True and e.sellados_int == True and e.lana == True and e.pintura == True:
                completo_mod += 1
        try:
            G1_prom = round(montado_mod / total_mod * 100)
        except ZeroDivisionError: 
            G1_prom = 0
        try:
            G2_prom = round(completo_mod / total_mod * 100)
        except ZeroDivisionError: 
            G2_prom = 0


        fechas = []
        for e in charts_data:
            if e.fecha_montado != None:
                fechas.append(e.fecha_montado.strftime("%Y-%m-%d"))
            fechas.sort()
        try:
            first = fechas[0]  # start date
        except IndexError:
            first = 0
        try:
            last = fechas[-1]   # end date
        except IndexError:
            last = 0
        G5_labels = [d.strftime("%Y-%m-%d") for d in pd.bdate_range(first, last)]
        G5_values = []
        for l in G5_labels:
            G5_values.append(fechas.count(l))
        recepcion = []
        for e in charts_data:
            if e.fecha_recibido != None:
                recepcion.append(e.fecha_recibido.strftime("%Y-%m-%d"))
        G5_recepcion = []
        for m in G5_labels:
            G5_recepcion.append(recepcion.count(m))
        G5_prom = round(sum(G5_values)/len(G5_values),1)
        recibidos = 0
        for s in charts_data:
            if s.recibido == True:
                recibidos += 1
        no_apto = 0
        for s in charts_data:
            if s.apto == False:
                no_apto += 1
        
           
        context['total_mod'] = total_mod
        context['montado_mod'] = montado_mod
        context['completo_mod'] = completo_mod
        context['ratio'] = G5_prom
        try:
            context['ratio_efectivo'] = round(montado_mod/len(set(fechas)),1)
        except ZeroDivisionError: 
            context['ratio_efectivo'] = 0
        context['G1_prom'] = G1_prom
        context['G2_prom'] = G2_prom
        context['G5_labels'] = G5_labels
        context['G5_values'] = G5_values
        context['G5_recepcion'] = G5_recepcion
        context['G5_prom'] = [round(G5_prom,)] * len(G5_labels)
        context['stock_apto'] = recibidos - montado_mod - no_apto
        context['stock_total'] = recibidos - montado_mod
        
        
        return context
 

# ------------------------------------------------------------------------------------------ Obra Vista

class ObraVista(DetailView):
    model = Obra
    template_name = 'obra/obra_vista.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = Montaje.objects.filter(modulo__obra=self.get_object())
        return context

class VistaUpdate(UpdateView):
    model = Montaje
    form_class = MontajeForm
    template_name = 'obra/mod.html'

    def get_success_url(self):
        return reverse_lazy('obra:vista', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = self.model.objects.all()
        return context

class MultipleUpdate(UpdateView):
    model = Montaje
    form_class = MontajeForm
    template_name = 'obra/mod.html'

    def get_success_url(self):
        return reverse_lazy('obra:vista', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = self.model.objects.all()
        return context

# ------------------------------------------------------------------------------------------ Obra Planilla

class ObraPlanilla(DetailView):
    model = Obra
    template_name = 'obra/obra_planilla.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = Montaje.objects.filter(modulo__obra=self.get_object())
        return context

class PlanillaUpdate(UpdateView):
    model = Montaje
    form_class = MontajeForm
    template_name = 'obra/modulo.html'

    def get_success_url(self):
        return reverse_lazy('obra:planilla', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modulos'] = self.model.objects.all()
        return context

"""def export_data(request):
    if request.method == 'POST':
        name = "attachment; filename={}.xls".format(str(date.today()))
        # Get selected option from form
        comment_resource = MontajeResources()
        dataset = comment_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = name
        return response   
    return render(request, 'obra/export_data_page.html') """


def export_excel(request):
    filtro = request.META['HTTP_REFERER'][-13:-9]
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}_{}.xls".format(filtro,str(date.today()))
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('DATOS_MONTAJE_TORRE') 
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'piso', 'posicion', 'modulo', 'identificador', 'fecha_montado', 'anclajes', 'lana',
        'pintura', 'sellados_int', 'observaciones'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Montaje.objects.filter(modulo__obra__obra_id=filtro).values_list(
        'piso', 'posicion', 'modulo__modulo', 'identificador', 'fecha_montado', 'anclajes', 'lana',
        'pintura', 'sellados_int', 'observaciones'
    )
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

# ------------------------------------------------------------------------------------------ Obra Recepcion

class ObraRecepcion(DetailView):
    model = Obra
    template_name = 'obra/obra_recepcion.html'

    def get_success_url(self):
        return reverse_lazy('obra:recepcion', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modfab'] = Montaje.objects.filter(modulo__obra=self.get_object(), estado='fabrica')
        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            for x in id_list:
                Montaje.objects.filter(pk=int(x)).update(recibido=True, estado='recibido', fecha_recibido=date.today())
            return self.get(request, *args, **kwargs)
       
# ------------------------------------------------------------------------------------------ Obra Montaje

class ObraMontaje(DetailView):
    model = Obra
    template_name = 'obra/obra_montaje.html'

    def get_success_url(self):
        return reverse_lazy('obra:montaje', args=[self.object.modulo.obra.obra_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modmon'] = Montaje.objects.filter(modulo__obra=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            fecha = request.POST.get('fecha')
            id_montado = request.POST.getlist('montado')
            id_anclajes = request.POST.getlist('anclajes')
            id_sellados = request.POST.getlist('sellados')
            id_lana = request.POST.getlist('lana')
            id_pintura = request.POST.getlist('pintura')
            identificador_list = dict(zip(request.POST.getlist('id'), request.POST.getlist('identificador')))
            for x in id_montado:
                p = Montaje.objects.get(pk=int(x)).fecha_montado
                if p == None:
                    Montaje.objects.filter(pk=int(x)).update(fecha_montado=fecha, estado='montado')
            for x in id_anclajes:
                Montaje.objects.filter(pk=int(x)).update(anclajes=True)
            for x in id_sellados:
                Montaje.objects.filter(pk=int(x)).update(sellados_int=True)
            for x in id_lana:
                Montaje.objects.filter(pk=int(x)).update(lana=True)
            for x in id_pintura:
                Montaje.objects.filter(pk=int(x)).update(pintura=True)
            for key, value in identificador_list.items():
                if value != "":
                    Montaje.objects.filter(pk=int(key)).update(identificador=value)
            return self.get(request, *args, **kwargs)

# ------------------------------------------------------------------------------------------ Obra Recursos

class ObraRecursos(DetailView):
    model = Obra
    template_name = 'obra/obra_recursos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operarios'] = Operario.objects.filter(obra_actual=self.get_object())
        return context

