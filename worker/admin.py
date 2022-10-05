from django.contrib import admin
from .models import User, Category, workeruser, albumTrabajos, photosTrabajos, review
# Register your models here.
admin.site.register(User)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'id')

admin.site.register(Category, CategoryAdmin)

class workeruserAdmin(admin.ModelAdmin):
    list_display = ('user', 'photoProfile','city','location' , 'phone', 'get_categorys')

admin.site.register(workeruser, workeruserAdmin)

class albumTrabajosAdmin(admin.ModelAdmin):
    list_display = ('owner',)

admin.site.register(albumTrabajos, albumTrabajosAdmin)

class photosTrabajosAdmin(admin.ModelAdmin):
    list_display = ('album', 'photos')

admin.site.register(photosTrabajos, photosTrabajosAdmin)

class reviewAdmin(admin.ModelAdmin):
    list_display = ('comentary', 'priceStar', 'puntualityStar','dealStar','workeruser','user')

admin.site.register(review, reviewAdmin)