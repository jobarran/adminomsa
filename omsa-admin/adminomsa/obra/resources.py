from xml.dom.pulldom import PROCESSING_INSTRUCTION
from import_export import resources, widgets
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Obra, Modulo, Montaje

class ForeignkeyRequiredWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            print(self.field, value)
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value})
        else:
            raise ValueError(self.field+ " required")

class ObraResources(resources.ModelResource):
    
    class Meta:
        model = Obra
        fields = ('obra', 'obra_id', 'pisos', 'posiciones', 'imagen',
            'estado', 'obra_link', 'ingenieria_obra')
        clean_model_instances = True

class ModuloResources(resources.ModelResource):
    
    class Meta:
        model = Modulo
        fields = ('obra', 'modulo', 'ingenieria')
        clean_model_instances = True

class MontajeResources(resources.ModelResource):
    piso = Field(attribute='piso', column_name='PISO')
    posicion = Field(attribute='posicion', column_name='Posicion')
    modulo = Field(attribute='modulo', column_name='Modulo', widget=ForeignKeyWidget(Modulo, 'modulo'))
    identificador = Field(attribute='identificador', column_name='N° Orden')
    control = Field(column_name='Control')
    fecha_montado = Field(attribute='fecha_montado', column_name='Montaje')
    empresa = Field(column_name='Empresa')
    anclajes = Field(attribute='anclajes', column_name='Colocacion de anclajes y pistas de arranque')
    tratamiento_ancl = Field(column_name='Tratamiento de Anclajes')
    lana = Field(attribute='lana', column_name='Colocación Lana Corta fuego', widget=widgets.BooleanWidget())
    pintura = Field(attribute='pintura', column_name='Colocación Pintura Cortahumo', widget=widgets.BooleanWidget())
    sellados_int = Field(attribute='observacuibes', column_name='Sellados Interiores', widget=widgets.BooleanWidget())
    observaciones = Field(attribute='sellados_int', column_name='Observaciones')
    remito = Field(attribute='remito', column_name='Remito')

    class Meta:
        model = Montaje
        fields = ('id', 'piso', 'posicion', 'modulo', 'identificador', 'control',
            'fecha_montado', 'empresa', 'anclajes', 'tratamiento_ancl', 'lana',
            'pintura', 'sellados_int', 'observaciones', 'remito')
        clean_model_instances = True