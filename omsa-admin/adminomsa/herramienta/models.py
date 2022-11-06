from enum import unique
from django.db import models
from obra.models import Obra

# Create your models here.
def custom_upload_to(instance, filename):
    old_instance = Herramienta.objects.get(pk=instance.pk)
    old_instance.imagen.delete()
    return 'herramienta/' + filename

class Herramienta(models.Model):

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

    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=20)
    identificador = models.CharField(max_length=30, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOISE)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOISE)
    imagen = models.ImageField(upload_to=custom_upload_to, default='herramienta/avatar.jpg', null=True, blank=True)
    obra_actual = models.ForeignKey(Obra, on_delete=models.PROTECT)
    observaciones = models.TextField(max_length=50, null=True, blank=True)


    slug = models.SlugField(max_length=30, null=True, blank=True) # Repetir ID

    def save(self, *args, **kwargs):
        self.slug = self.identificador
        super(Herramienta, self).save(*args, **kwargs)

    class Meta:
        ordering = ['marca']

    def __str__(self):
         return self.nombre + " - " + self.marca