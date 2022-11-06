from django.urls import path
from .views import HerramientaListView, HerramientaCreate, HerramientaUpdate
herramienta_patterns = ([
    path('', HerramientaListView.as_view(), name='herramienta'),
    path('new/create/', HerramientaCreate.as_view(), name='create'),
    path('<slug>/', HerramientaUpdate.as_view(), name='update'),
], 'herramienta')
