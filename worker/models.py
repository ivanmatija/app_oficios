from urllib.request import Request
from django.conf import settings
from location_field.models.plain import PlainLocationField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.forms import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractUser):
    is_workeruser = models.BooleanField(default=False)





# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, help_text="ingrese la categoria")
    active = models.BooleanField(default=True)
    icon = models.ImageField(upload_to='iconos', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'



class workeruser(models.Model):
    name = models.CharField(max_length=200, help_text="ingresá tu nombre")
    lastname = models.CharField(max_length=200, help_text="ingresá tu apellido")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name ='profile')
    photoProfile = models.ImageField(upload_to='fotoperfil', null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    phone = PhoneNumberField()
    category = models.ManyToManyField(Category, help_text="Seleccione una categoria")
    city = models.CharField(max_length=200, help_text="ingrese la localidad")
    description = models.TextField(blank=False,null=False)
    
    
    def get_categorys(self):
        return ",".join([str(p) for p in self.category.all()])

    class Meta:
        db_table = 'workeruser'

    def __str__(self):
        return str(self.id)

@receiver(post_save, sender=workeruser)
def asignar_al_user(sender, instance, **kwargs):
    user_id = instance.user.id
    user_a = User.objects.get(id=user_id)
    user_a.is_workeruser = 'True'
    user_a.save()


class albumTrabajos(models.Model):
    owner = models.OneToOneField(workeruser, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'albumTrabajos'



class photosTrabajos(models.Model):
    album =models.ForeignKey(albumTrabajos, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='fotosTrabajos', null=True)
    
    class Meta:
        db_table = 'photosTrabajos'

class review(models.Model):
    STAR_RATING_CHOICES = (
    (1, '$'),
    (2, '$$'),
    (3, '$$$'),
    (4, '$$$$'),
    (5, '$$$$$'),
    )
    comentary = models.CharField(max_length=255, null=True, blank=True)
    priceStar = models.IntegerField(choices=STAR_RATING_CHOICES)
    puntualityStar = models.IntegerField(choices=STAR_RATING_CHOICES)
    dealStar = models.IntegerField(choices=STAR_RATING_CHOICES)
    workeruser = models.ForeignKey(workeruser, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'review'