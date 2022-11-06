from django.db import models
from collections import Counter

# -----------------------------------------------------------------------------------------  Obra

def custom_upload_to(instance, filename):
    old_instance = Obra.objects.get(pk=instance.pk)
    old_instance.imagen.delete()
    return 'obra/' + filename

class Obra(models.Model):

    ESTADO_CHOISE = (
        ('Proxima', 'Proxima'),
        ('Ejecucion', 'Ejecucion'),
        ('Terminada', 'Terminada'),
    )

    obra = models.CharField(max_length=50)
    obra_id = models.CharField(max_length=4)
    pisos = models.IntegerField()
    posiciones = models.IntegerField()
    imagen = models.ImageField(upload_to=custom_upload_to, default='obra/avatar_b.jpg', null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOISE)
    ingenieria_obra = models.FileField(null=True, blank=True)  # subir archivos PDF

    slug = models.SlugField(max_length=4) # Repetir ID

    class Meta:
        ordering = ['obra_id']

    def __str__(self):
         return self.obra


# -----------------------------------------------------------------------------------------  Modulos y monaje

class Modulo(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    modulo = models.CharField(max_length=50, null=True, blank=True)
    ingenieria_modulo = models.FileField(null=True, blank=True)  # subir archivos PDF 

    def __str__(self):
         return self.modulo

class Montaje(models.Model):
    piso = models.CharField(max_length=5,)
    posicion = models.IntegerField()
    modulo = models.ForeignKey(Modulo, on_delete=models.PROTECT)
    identificador = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=50, default='fabrica')
    fecha_montado = models.DateField(null=True, blank=True)
    fecha_recibido = models.DateField(null=True, blank=True)
    anclajes = models.BooleanField(default=False)
    sellados_int = models.BooleanField(default=False)
    lana = models.BooleanField(default=False)
    pintura = models.BooleanField(default=False)
    recibido = models.BooleanField(default=False)
    observaciones = models.TextField(max_length=50, null=True, blank=True)
    reposicion = models.BooleanField(default=False)
    reposicion_obs = models.CharField(max_length=30, null=True, blank=True)
    remito = models.IntegerField(null=True, blank=True)
    apto = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Montaje'
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        
        if self.recibido == False:
            self.estado = 'fabrica'
        if self.fecha_montado == None and self.recibido == True and self.apto == True:
            self.estado = 'recibido'
        if self.fecha_montado != None:
            self.estado = 'montado'
        if self.fecha_montado != None and self.lana == True and self.anclajes == True and self.pintura == True and self.sellados_int == True:
            self.estado = 'completo'
        if self.reposicion == True :
            self.estado = 'incompleto'
        if self.identificador == None and self.fecha_montado != None:
            self.estado = 'falta_id'
        if self.apto == False:
            self.estado = 'no_apto'
        super(Montaje, self).save(*args, **kwargs)

        identlist = list(Montaje.objects.filter(modulo__obra__obra_id=self.modulo.obra.obra_id).values_list('identificador', flat=True))
        d = Counter(identlist)
        dupes = list([item for item in d if d[item]>1])
        idlist = Montaje.objects.filter(modulo__obra__obra_id=self.modulo.obra.obra_id)
        for i in idlist.iterator():
            if i.identificador != None:
                if i.estado == 'repetido':
                    if i.recibido == False:
                        i.estado = 'fabrica'
                    if i.fecha_montado == None and i.recibido == True and i.apto == True:
                        i.estado = 'recibido'
                    if i.fecha_montado != None:
                        i.estado = 'montado'
                    if i.fecha_montado != None and i.lana == True and i.anclajes == True and i.pintura == True and i.sellados_int == True:
                        i.estado = 'completo'
                    if i.reposicion == True :
                      i.estado = 'incompleto'
                    if i.identificador == None and i.fecha_montado != None:
                        i.estado = 'falta_id'
                    if i.apto == False:
                        i.estado = 'no_apto'
                    super(Montaje, i).save(*args, **kwargs)         
                if i.identificador in dupes:
                    i.estado = 'repetido'
                    super(Montaje, i).save(*args, **kwargs)


                    
    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})

    # -----------------------------------------------------------------------------------------  Recepcion de modulos

