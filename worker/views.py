from msilib.schema import ListView
from unicodedata import category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import workeruserForm
from .models import Category, workeruser, User, review
from order.models import orderQuote, QuoteResponse
from django.views import generic
from django.views.generic import CreateView, UpdateView
from django.http import Http404 , request
from operator import and_ , or_
from django.db.models import Q
from functools import reduce


from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest

from django.core import serializers
import json

from fcm_django.models import FCMDevice

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
   body = request.body.decode('utf-8')
   bodyDict = json.loads(body)

   token = bodyDict['token']

   existe =FCMDevice.objects.filter(registration_id = token , active=True)
   if len(existe) > 0:
      return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))

   dispositivo = FCMDevice()
   dispositivo.registration_id = token
   dispositivo.active = True

   if request.user.is_authenticated:
      dispositivo.user = request.user

      try:
         dispositivo.save()
         return HttpResponse(json.dumps({'mensaje':'token guardado'}))
      except:
         return HttpResponseBadRequest(json.dumps({'mensaje':'No se ha podido guardar el token'}))




class categoryListView(generic.ListView):
   model = Category
   template_name = 'index.html'


   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      userr = self.request.user.id
      #print(userr)
      worker = list(workeruser.objects.filter(user_id = userr).values_list("id", flat = True))
      worker.append(0)
      obtengoworkeruser = workeruser.objects.filter(user_id=userr)
      categoriasdelworker = list(obtengoworkeruser.values_list('category',flat=True))
      orderlistwithresponse = list(QuoteResponse.objects.filter(workeruser_id=worker[0]).values_list('orderQuote_id',flat=True))
      categoriasdelworker.append(0)
      orderlistwithresponse.append(0)
      #print(categoriasdelworker)
      context['order_list'] =  orderQuote.objects.filter(is_order='False').filter(reduce(or_, [Q(category_id=c) for c in categoriasdelworker]))
      context['orderwithoutresponse_list'] = orderQuote.objects.filter(is_order='False').filter(reduce(or_, [Q(category_id=c) for c in categoriasdelworker])).exclude(reduce(or_, [Q(id=c) for c in orderlistwithresponse]))
      context['orderwithresponse_list'] =  orderQuote.objects.filter(is_order='False').filter(reduce(or_, [Q(category_id=c) for c in categoriasdelworker])).filter(reduce(or_, [Q(id=c) for c in orderlistwithresponse]))
      #print(context)
      #print(categoriasdelworker)
      #print(QuoteResponse.objects.filter(workeruser_id=dataworkeruserid).values())
      #print(orderQuote.objects.filter(is_order='False').values())
      return context
 

def sosprofesional(request):
   servicios = Category.objects.all()
   context = {
      'category_list':servicios
   }
   return render(request, 'sosprofesional.html',context)

def comofunciona(request):
   servicios = Category.objects.all()
   context = {
      'category_list':servicios
   }
   return render(request, 'comofunciona.html', context)

def comofuncionaprofesional(request):
   servicios = Category.objects.all()
   context = {
      'category_list':servicios
   }
   return render(request, 'comofuncionaprofesional.html', context)
   
def comofuncionacotizar(request):
   servicios = Category.objects.all()
   context = {
      'category_list':servicios
   }
   return render(request, 'comofuncionacotizar.html', context)

class crearworkeruser(LoginRequiredMixin, CreateView):
   model = workeruser
   form_class = workeruserForm
   template_name = 'formularioworkeruser.html'
   success_url = 'index'
   

   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


   
class workerListView(generic.ListView):
   model = workeruser
   template_name = 'mostrartrabajadores.html'
   
   def get(self, request, *args, **kwargs):
        # either
        self.object_list = self.get_queryset()
        self.object_list = self.object_list.filter(category__id=kwargs['id'])
         
        # or
        queryset = Category.objects.filter(id=kwargs['id'])
        if queryset.exists():
            self.object_list = self.object_list.filter(category__id=kwargs['id'])
        else:
            raise Http404("no hay trabajadores en esta categoria")

        # in both cases
        context = self.get_context_data()
        return self.render_to_response(context)   

class editarperfilUpdateView(LoginRequiredMixin, UpdateView):
   model = workeruser
   form_class = workeruserForm
   template_name = 'formularioworkeruser.html'
   success_url = '/index'

   def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user_id=self.request.user
        )


class workeruserprofileListView(generic.ListView):
   model = workeruser
   template_name = 'workeruserprofile.html'

   def get_context_data(self, **kwargs):
      context = super(workeruserprofileListView, self).get_context_data(**kwargs)
      
      context['worker'] =  workeruser.objects.filter(id=self.kwargs.get('id'))
      context['reseña'] =  review.objects.filter(workeruser_id=self.kwargs.get('id'))
      print(context)
      return context