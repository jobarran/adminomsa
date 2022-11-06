from django.urls import path
from .views import ObraListView, ObraDetailView, PlanillaUpdate, ObraPlanilla, ObraVista, VistaUpdate, ObraCreate, export_excel, ObraRecepcion, ObraMontaje, ObraRecursos, ObraUpdate

obra_patterns = ([
    path('', ObraListView.as_view(), name='obra'),
    path('<slug>/', ObraDetailView.as_view(), name='detail'),
    path('<slug>/planilla', ObraPlanilla.as_view(), name='planilla'),
    path('modulo/<int:pk>', PlanillaUpdate.as_view(), name='modulo'),
    path('<slug>/vista', ObraVista.as_view(), name='vista'),
    path('mod/<int:pk>', VistaUpdate.as_view(), name='mod'),
    path('new/create/', ObraCreate.as_view(), name='create'),
    path('<slug>/update', ObraUpdate.as_view(), name='update'),
    path('exp/export/', export_excel, name="export-excel"),
    path('<slug>/recepcion', ObraRecepcion.as_view(), name="recepcion"),
    path('<slug>/montaje', ObraMontaje.as_view(), name="montaje"),
    path('<slug>/recursos/', ObraRecursos.as_view(), name='recursos'),
], 'obra')
