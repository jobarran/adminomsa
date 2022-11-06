from asyncio.windows_events import NULL
from email.policy import default
from enum import unique
from logging.config import dictConfig
from django.db import models
from obra.models import Obra

# Create your models here.
def custom_upload_to(instance, filename):
    old_instance = Operario.objects.get(pk=instance.pk)
    old_instance.imagen.delete()
    return 'operario/' + filename

class Operario(models.Model):

    ESTADO_CHOISE = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )

    CATEGORIA_CHOISE = (
        ('Capataz', 'Capataz'),
        ('Especializado', 'Especializado'),
        ('Oficial', 'Oficial'),
        ('Medio Oficial', 'Medio Oficial'),
        ('Ayudante', 'Ayudante'), 
    )

    EMPRESA_CHOISE = (
        ('OMSA', 'OMSA'),
        ('CWI', 'CWI'),
        ('SUBCONTRATO', 'SUBCONTRATO'),
    )

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=20)
    legajo = models.IntegerField(unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOISE)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOISE, default='Activo')
    telefono = models.IntegerField(null=True, blank=True)
    imagen = models.ImageField(upload_to=custom_upload_to, default='operario/avatar.jpg', null=True, blank=True)
    obra_actual = models.ForeignKey(Obra, on_delete=models.PROTECT)
    dni = models.IntegerField(null=True, blank=True)
    nacimiento = models.DateField(null=True, blank=True)
    empresa = models.CharField(max_length=50, choices=EMPRESA_CHOISE, default='CWI')


    slug = models.SlugField(max_length=4, null=True, blank=True) # Repetir ID

    def save(self, *args, **kwargs):
        self.slug = self.legajo
        super(Operario, self).save(*args, **kwargs)

    class Meta:
        ordering = ['legajo']

    def __str__(self):
         return self.apellido + ", " + self.nombre

class Actividad(models.Model):
    id_tarea = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
         return self.nombre

class Dia(models.Model):

    fecha = models.DateField()
    estado = models.BooleanField(default=True)
    slug = models.SlugField(max_length=6, unique=True, null=True, blank=True) # ID
    
    def __str__(self):
         return str(self.fecha)
         
    class Meta:
        ordering = ['-id']

class Presentismo(models.Model):

    ESTADO_CHOISE = (
        ('Presente', 'Presente'),
        ('Ausente', 'Ausente'),
        ('Vacaciones', 'Vacaciones'),
        ('ART', 'ART'),
    )

    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    fecha = models.ForeignKey(Dia, on_delete=models.PROTECT)
    hora_ingreso = models.TimeField()
    hora_egreso =  models.TimeField()
    actividad = models.ForeignKey(Actividad, on_delete=models.PROTECT)
    observaciones = models.TextField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOISE, null=True, blank=True)
    cargado = models.BooleanField(default=False)

    def __str__(self):
         return self.operario.apellido +" "+ str(self.fecha)

    class Meta:
        ordering = ['fecha']