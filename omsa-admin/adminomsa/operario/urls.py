from django.urls import path
from .views import OperarioListView, OperarioUpdate, OperarioCreate, InactivoListView, DiaListView, DiaUpdate
operario_patterns = ([
    path('', OperarioListView.as_view(), name='operario'),
    path('fecha/', DiaListView.as_view(), name='fecha'),
    path('<slug>/', OperarioUpdate.as_view(), name='update'),
    path('new/create/', OperarioCreate.as_view(), name='create'),
    path('inactivo', InactivoListView.as_view(), name='inactivo'),
    path('fecha/<slug>/', DiaUpdate.as_view(), name='parte'),
], 'operario')
