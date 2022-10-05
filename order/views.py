from urllib.request import Request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from worker.models import workeruser, User
from .forms import quoteForm, QuoteResponseForm
from .models import orderQuote,QuoteResponse
from django.views import generic
from django.views.generic import CreateView
from django.db.models.functions import Round
from django.db.models import Avg
from operator import and_ , or_
from django.db.models import Q
from functools import reduce

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# Create your views here.
class crearquote(LoginRequiredMixin, CreateView):
   model = orderQuote
   form_class = quoteForm
   template_name = 'formularioquote.html'
   success_url = 'index'
   
   
   def form_valid(self, form):
      form.instance.user = self.request.user
      usere = list(workeruser.objects.filter(category=form.instance.category).values_list("user_id", flat=True))
      print(form.instance.category)
      device = FCMDevice.objects.filter(reduce(or_, [Q(user=c) for c in usere]))
      device.send_message(
      Message(notification=Notification(title="ServiciosYa", body="Han presupuestado su solicitud, revisa la bandeja de cotizaciones")
    ))
      return super().form_valid(form)

      """device.send_message(
      Message(
        data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark",
        "click_action" : "https://www.youtube.com/"
      }
    ))"""

class quoteListView(generic.ListView):
   model = orderQuote
   template_name = 'miscotizaciones.html'

   def get_queryset(self):
      return orderQuote.objects.filter(is_order='False',user=self.request.user)

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      promedio = Round(Avg('quoteresponse__price'))
      cantidad = Count('quoteresponse')
      context['object_list'] = orderQuote.objects.filter(is_order='False',user=self.request.user).aggregate(ave = Avg('quoteresponse__price'))
      
      
      context['object_list'] = orderQuote.objects.annotate(num_quoteResponse=cantidad).annotate(ave = promedio)
      #context['object_list'] = orderQuote.objects.annotate(ave = Round(Avg('quoteresponse__price')))
      context['response_list'] = QuoteResponse.objects.all()
      print(context)
      return context

class quotetomeListView(generic.ListView):
   model = orderQuote
   template_name = 'miscotizacionespedidas.html'

   def get_queryset(self):
      data = orderQuote.objects.all().values()
      userr = self.request.user.id
      worker = list(workeruser.objects.filter(user_id = userr).values_list("id", flat = True))
      print (self.request.user.id)
      print (data)
      return orderQuote.objects.filter(is_order='False',workeruser_id=worker[0])

class ordertomeListView(generic.ListView):
   model = orderQuote
   template_name = 'missolicitudespedidas.html'

   def get_queryset(self):
      data = orderQuote.objects.all().values()
      userr = self.request.user.id
      worker = list(workeruser.objects.filter(user_id = userr).values_list("id", flat = True))
      print (self.request.user.id)
      print (data)
      return orderQuote.objects.filter(is_order='True',workeruser_id=worker[0])


class crearQuoteResponse(LoginRequiredMixin, CreateView):
   model = QuoteResponse
   form_class = QuoteResponseForm
   template_name = 'formularioquoteresponse.html'
   success_url = '/index'

   def form_valid (self, form, *args, **kwargs):
      userr = self.request.user.id
      worker = list(workeruser.objects.filter(user_id = userr).values_list("id", flat = True))
      form.instance.orderQuote_id = self.kwargs['orderQuote_id']
      form.instance.workeruser_id = worker[0]

      #notification
      usere = list(orderQuote.objects.filter(id=self.kwargs['orderQuote_id']).values_list("user_id", flat=True))
      device = FCMDevice.objects.filter(user=usere[0])
      device.send_message(
      Message(
        notification=Notification(title="ServiciosYa", body="Han presupuestado su solicitud, revisa la bandeja de cotizaciones")
    ))
      return super().form_valid(form)
      """device.send_message(
      Message(
        data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark",
        "click_action" : "https://www.youtube.com/"
      }
    ))"""

    

   def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(**kwargs)
      context['quote_list'] =  orderQuote.objects.filter(is_order='False').filter(id = self.kwargs['orderQuote_id'])
      return context


class myorderListView(generic.ListView):
   model = orderQuote
   template_name = 'missolicitudes.html'

   def get_queryset(self):
      return orderQuote.objects.filter(is_order='True',user=self.request.user)

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['object_list'] = orderQuote.objects.filter(is_order='True',user=self.request.user)
      print(context)
      return context