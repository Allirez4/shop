from django import forms
from accounts.models import CustomUser
from home.models import Product
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=[
            'address','city','extrainfo','delivery_date'
        ]
    def __init__(self, *args, **kwargs):
        #self.fields['delivery_fee'].widget.attrs.update({'readonly': 'True'})
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
             