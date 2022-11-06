from django.shortcuts import render
from django.views.generic import TemplateView

# Definimos la clase Home y asignamos el template name
class HomePageView(TemplateView):
    template_name = 'core/home.html'

# A traves del metodo get le asignamos un titulo al contexto para poder usarlo en el template home.html
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title':'OMSA | CWI'})

class SamplePageView(TemplateView):
    template_name = 'core/sample.html'
