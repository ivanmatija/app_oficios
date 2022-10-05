from django.contrib import admin
from .models import orderQuote, QuoteResponse
# Register your models here.
class orderQuoteAdmin(admin.ModelAdmin):
    list_display = ('is_order', 'workeruser', 'user', 'status', 'date', 'workshift', 'price', 'location', 'name', 'phone', 'imageOrderQuote', 'description')

admin.site.register(orderQuote, orderQuoteAdmin)

class QuoteResponseAdmin(admin.ModelAdmin):
    list_display = ('workeruser', 'orderQuote', 'price', 'datePossible', 'workshiftPossible')

admin.site.register(QuoteResponse, QuoteResponseAdmin)