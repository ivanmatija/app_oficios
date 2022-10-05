"""mundodequimeras URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from worker import views
from order import views as viewsQuote

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('index/', views.categoryListView.as_view(), name='index'),
    path('', RedirectView.as_view(url='/index/', permanent=True)),
    path('sosprofesional', views.sosprofesional, name='sosprofesional'),
    path('comofunciona', views.comofunciona, name='comofunciona'),
    path('comofunciona/profesional', views.comofuncionaprofesional, name='comofunciona/profesional'),
    path('comofunciona/cotizar', views.comofuncionacotizar, name='comofunciona/cotizar'),
    #crear Workeruser
    path('neworkeruser',views.crearworkeruser.as_view(),name='neworkeruser'),
    #actualizar worker user
    path('updateworkeruser/<pk>',views.editarperfilUpdateView.as_view(),name='updateworkeruser'),
    #crear cotizacion
    path('newquote',viewsQuote.crearquote.as_view(),name='newquote'),
    #crear respuesta a cotizacion
    path('newquoteresponse/<orderQuote_id>',viewsQuote.crearQuoteResponse.as_view(),name='newquoteresponse'),
    #apartado mis cotizaciones
    path('quotesofmine/',viewsQuote.quoteListView.as_view(),name='quotesofmine'),
    #mis solicitudes
    path('orderofmine/',viewsQuote.myorderListView.as_view(),name='orderofmine'),
    #mostrar perfil del trabajador
    path('workerprofile/<id>',views.workeruserprofileListView.as_view(),name='workerprofile'),
    #mostrar los trabajadores de cada categoria
    path('showorkers/<id>', views.workerListView.as_view(), name='showorkers'),
    #mostrar las cotizaciones que me pidieron a mi
    path('quotestome/',viewsQuote.quotetomeListView.as_view(),name='quotestome'),
    #mostrar las solicitudes que me pidieron a mi
    path('orderstome/',viewsQuote.ordertomeListView.as_view(),name='orderstome'),
    path('', include('pwa.urls')),
    path('guardar-token/',views.guardar_token,name='guardar_token'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


