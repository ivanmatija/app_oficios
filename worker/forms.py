from dataclasses import fields
from tkinter import Widget
from django import forms
from location_field.forms.plain import PlainLocationField
from worker.models import workeruser
from .models import workeruser


class workeruserForm(forms.Form, forms.ModelForm ):
    location=PlainLocationField(based_fields=['city'],initial='-22.2876834,-49.1607606')
    class Meta:
        model = workeruser
        fields = ['phone','category','city','photoProfile','description']
        labels = {
            'phone':'Nro de celular',
            'category':'seleccioná los servicios que prestas',
            'city':'localidad',
            'photoProfile':'foto de perfil',
            'description':'descripción',
        }
        widgets = {
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
        }
        