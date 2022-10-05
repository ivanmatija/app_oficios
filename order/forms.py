from dataclasses import fields
from tkinter import Widget
from django import forms
from .models import QuoteResponse, orderQuote


class quoteForm(forms.Form, forms.ModelForm ):
    class Meta:
        model = orderQuote
        fields = ['workshift','name','phone','imageOrderQuote','description','asunto','category',]
        labels = {
            'phone':'Nro de celular',
            'category':'seleccioná la categoria',
            'workshift':'turno',
            'imageOrderQuote':'foto',
            'description':'descripción',
            'name':'nombre de la persona que va a recibir al profecional',
            'asunto':'ingrese un asunto',
        }
        """widgets = {
            'city':forms.TextInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'ingresá tu localidad',
                    'id':'location'
                }
            ),
            'address':forms.TextInput(
                attrs= {
                    'class':'form-control',
                    'placeholder':'ingresá tu dirección(calle y altura)',
                    'id':'address'
                }
            ),
            'description':forms.Textarea(
                attrs= {
                    'class':'form-control',
                    'placeholder':'escribí una breve descripción de tu perfil profesional',
                    'id':'description'
                }
            ),
        }"""

class QuoteResponseForm(forms.Form, forms.ModelForm ):
    class Meta:
        model = QuoteResponse
        fields = ['price','datePossible','workshiftPossible',]
        labels = {
            'price':'Precio',
            'datePossible':'que dia estas dispuesto a ir',
            'workshiftPossible':'turno',
        }
        widgets = {"workeruser_id": forms.HiddenInput()}