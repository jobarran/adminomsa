from django import forms
from .models import Operario, Presentismo


class OperarioForm(forms.ModelForm):

    class Meta:
        model = Operario
        fields = [
            'nombre', 'apellido', 'legajo', 'estado', 'categoria', 'telefono', 'imagen', 'obra_actual', 'dni', 'nacimiento', 'empresa'
            ]
        ESTADO_CHOICES = (
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
            )
        CATEGORIA_CHOICES = (
            ('Capataz', 'Capataz'),
            ('Especializado', 'Especializado'),
            ('Oficial', 'Oficial'),
            ('Medio Oficial', 'Medio Oficial'),
            ('Ayudante', 'Ayudante'),
            )
        EMPRESA_CHOISES = (
            ('OMSA', 'OMSA'),
            ('CWI', 'CWI'),
        )
        widgets = {
            'legajo': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Legajo', 'type':'number'}),
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}),
            'estado' : forms.Select(choices=ESTADO_CHOICES,attrs={'class': 'form-control'}),
            'categoria' : forms.Select(choices=CATEGORIA_CHOICES,attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Telefono', 'type':'number'}),
            'imagen' : forms.FileInput(attrs={'class':'form-control', 'placeholder': ''}),
            'dni' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'DNI', 'type':'number'}),
            'nacimiento' : forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text', 'class':'form-control myDateClass', 'placeholder':'Fecha de Nacimiento', 'onfocus':"(this.type='date')"}),
            'obra_actual': forms.Select(attrs={'class': 'form-control'}),
            'empresa' : forms.Select(choices=EMPRESA_CHOISES,attrs={'class': 'form-control'}),
        }


class PresentismoForm(forms.ModelForm):

    class Meta:
        model = Presentismo
        fields = [
            'operario', 'obra', 'fecha', 'hora_ingreso', 'hora_egreso', 'actividad', 'observaciones', 'estado', 'cargado'
            ]
        ESTADO_CHOICES = (
            ('Presente', 'Presente'),
            ('Ausente', 'Ausente'),
            ('Vacaciones', 'Vacaciones'),
            ('ART', 'ART'),
        )
        widgets = {
            'operario': forms.Select(attrs={'class': 'form-control'}),
            'obra': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'text', 'class':'form-control myDateClass', 'placeholder':'Fecha montados', 'onfocus':"(this.type='date')"}),
            'hora_ingreso' : forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'})),
            'hora_egreso' : forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'})),
            'actividad': forms.Select(attrs={'class': 'form-control'}),
            'observaciones' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'IRPI - IRCO'}),
            'estado' : forms.Select(choices=ESTADO_CHOICES,attrs={'class': 'form-control'}),
        }