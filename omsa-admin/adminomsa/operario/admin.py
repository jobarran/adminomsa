from django.contrib import admin
from .models import Operario, Actividad, Presentismo, Dia

# Register your models here.
class OperarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'legajo', 'estado', 'categoria', 'telefono', 'imagen', 'obra_actual')

    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('id_tarea', 'nombre', 'descripcion')

    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

class DiaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'estado', 'slug')

    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

class PresentismodAdmin(admin.ModelAdmin):
    list_display = ('operario', 'obra', 'fecha', 'hora_ingreso', 'hora_egreso', 'actividad', 'observaciones', 'estado', 'cargado')

    class Media:
        css = {
            'all': ('obras/css/custom_ckeditor.css',)
        }

admin.site.register(Operario, OperarioAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Dia, DiaAdmin)
admin.site.register(Presentismo, PresentismodAdmin)