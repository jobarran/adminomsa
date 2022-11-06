from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Obra, Modulo, Montaje
from .resources import ObraResources, ModuloResources, MontajeResources

# Register your models here.

# Register your models here.

class ObraAdmin(ImportExportModelAdmin):
    resource_class = ObraResources
    list_display = ('id', 'obra', 'obra_id', 'pisos', 'posiciones', 'imagen',
            'estado', 'ingenieria_obra')
    
    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

class ModuloAdmin(ImportExportModelAdmin):
    resource_class = ModuloResources
    list_display = ('obra', 'modulo', 'ingenieria_modulo')
    
    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

class MontajeAdmin(ImportExportModelAdmin):
    resource_class = MontajeResources
    list_display = ('piso', 'posicion', 'modulo', 'identificador',
            'estado', 'fecha_montado', 'fecha_recibido', 'anclajes', 'sellados_int',
            'lana', 'pintura', 'recibido', 'observaciones', 'reposicion',
            'reposicion_obs', 'remito', 'date_modified')
    
    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }


admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(Montaje, MontajeAdmin)