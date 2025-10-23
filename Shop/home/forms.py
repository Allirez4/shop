from django import forms
from accounts.models import CustomUser

class profileUpdate(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields=['full_name','email','phone_number','city','address','postal_code','national_code']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})