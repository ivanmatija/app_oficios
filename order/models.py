from django.conf import settings
from location_field.models.plain import PlainLocationField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
#from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
from worker.models import workeruser,Category


# Create your models here.
class orderQuote(models.Model):
    workeruser = models.ForeignKey(workeruser, on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #no se si poner related_name=profile y el unique=true
    STATUS =(
        ('1', 'is waiting response'),
        ('2','have date'),
        ('3','is confirmed'),
        ('4','is paid'),
        ('5','warranty requested'),
        ('6','completed coverage'),
        ('7','absense'),
        ('8','rearreglo hecho'),
        ('9','rearreglo confirmado'),
        ('10','disconformidad de rearreglo'),
    )
    status = models.CharField(max_length=2, choices=STATUS, blank=True, default='1', help_text='Estado de la orden')
    date = models.DateField(blank=True,null=True)
    WORKSHIFT =(
        ('m', 'de 8 a 12'),
        ('s','de 14 a 17'),
        ('t','de  17 a 21'),
        ('u','urgente'),
    )
    workshift = models.CharField(max_length=2, choices=WORKSHIFT, default='m', help_text='Turno')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    is_order = models.BooleanField(default=False)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    #address = map_fields.AddressField(max_length=200)
    #geolocation = map_fields.GeoLocationField(max_length=100)
    name = models.CharField(max_length=200, help_text="persona que va a recibir al trabajador")
    phone = PhoneNumberField()
    imageOrderQuote = models.ImageField(upload_to='cotizaciones-pedidos', null=True)
    asunto = models.CharField(max_length=200, help_text="asunto del pedido")
    description = models.CharField(max_length=500, help_text="descripcion del pedido")
    category = models.ForeignKey(Category, help_text="Seleccione una categoria",on_delete=models.CASCADE)
        
    class Meta:
        db_table = 'orderQuote'

class QuoteResponse(models.Model):
    workeruser = models.ForeignKey(workeruser, on_delete=models.CASCADE, unique=False, related_name ='workeruser_id')
    orderQuote = models.ForeignKey(orderQuote, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    datePossible = models.DateField()
    WORKSHIFTPOSSIBLE =(
        ('m', 'de 8 a 12'),
        ('s','de 14 a 17'),
        ('t','de  17 a 21'),
        ('u','urgente'),
    )
    workshiftPossible = models.CharField(max_length=2, choices=WORKSHIFTPOSSIBLE, default='m', help_text='Turno')
    class Meta:
        db_table = 'QuoteResponse'

    def __str__(self):
        return str(self.workeruser)
