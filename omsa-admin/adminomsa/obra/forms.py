from django import forms
from .models import Montaje, Obra


class ObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = [
            'obra', 'obra_id', 'pisos',
            'posiciones', 'imagen', 'estado', 'ingenieria_obra', 'slug'
            ]
        ESTADO_CHOICES = (
                ('Proxima', 'Proxima'),
                ('Ejecucion', 'Ejecucion'),
                ('Terminada', 'Terminada'),
                )
        widgets = {
            'obra': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'obra_id': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ID', 'type':'number'}),
            'pisos': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pisos', 'type':'number'}),
            'posiciones': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Posiciones', 'type':'number'}),
            'imagen' : forms.FileInput(attrs={'class':'form-control', 'placeholder': ''}),
            'estado' : forms.Select(choices=ESTADO_CHOICES,attrs={'class': 'form-control'}),
            'ingenieria_obra': forms.FileInput(attrs={'class':'form-control', 'placeholder':'Ingenieria'}),
            'slug' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ID', 'type':'number'}),
        }

class MontajeForm(forms.ModelForm):

    class Meta:
        model = Montaje
        fields = [
            'identificador', 'fecha_montado', 'fecha_recibido',
            'anclajes', 'sellados_int', 'lana', 'pintura', 'recibido', 'observaciones', 'reposicion', 'reposicion_obs', 'apto'
            ]
        widgets = {
            'identificador': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ID', 'type':'number'}),
            'fecha_montado': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text', 'class':'form-control myDateClass', 'placeholder':'Fecha montados', 'onfocus':"(this.type='date')"}),
            'fecha_recibido': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text', 'class':'form-control myDateClass', 'placeholder':'Fecha recibido', 'onfocus':"(this.type='date')"}),
            'anclajes': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'sellados_int': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lana': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'pintura': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'recibido': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'observaciones': forms.Textarea(attrs={'rows':2, 'class':'form-control', 'placeholder':'Observaciones'}),
            'reposicion': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'reposicion_obs': forms.TextInput(attrs={'class':'form-control', 'placeholder':'IRPI - IRCO'}),
            'apto': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


