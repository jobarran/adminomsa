from django import forms
from .models import Herramienta


class HerramientaForm(forms.ModelForm):

    class Meta:
        model = Herramienta
        fields = [
            'nombre', 'marca', 'identificador', 'categoria', 'estado', 'imagen', 'obra_actual', 'observaciones'
            ]
        ESTADO_CHOISE = (
            ('Nuevo', 'Nuevo'),
            ('Bueno', 'Bueno'),
            ('Medio', 'Medio'),
            ('Regular', 'Regular'),
            ('Malo', 'Malo'),
            ('Baja', 'Baja'),
        )

        CATEGORIA_CHOISE = (
            ('Electrica', 'Electrica'),
            ('Manual', 'Manual'),
            ('Equipo', 'Equipo'),
        )

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'marca': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Marca'}),
            'identificador': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Identificador'}),
            'categoria' : forms.Select(choices=CATEGORIA_CHOISE,attrs={'class': 'form-control'}),
            'estado' : forms.Select(choices=ESTADO_CHOISE,attrs={'class': 'form-control'}),
            'imagen' : forms.FileInput(attrs={'class':'form-control', 'placeholder': ''}),
            'obra_actual': forms.Select(attrs={'class': 'form-control'}),
            'observaciones' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Observaciones', 'rows':'3'}),
        }

