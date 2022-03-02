from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, ValidationError
from .models import Holding
from .helper_functions import txtToArray
from datetime import date
from django.utils.translation import gettext_lazy as _

# Add new position
class HoldingForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'tags', 'placeholder':'Coin', 'data-bs-toggle':"tooltip", 'data-bs-placement':"top", 'title':"Use an auto-suggestion below"}))
    use_mv_entry = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'use_mv_entry', 'name':"use_mv_entry"}), label="use market price", initial=False, required=False)
    class Meta:
        model = Holding
        fields = ('name', 'entry_price', 'entry_amount')

        widgets = {
            'coin_id': forms.TextInput(attrs={'class':'form-control', 'id':'tags', 'placeholder':'Coin (choose from below)'}),
            'entry_price': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Entry Price', 'name':'entry-price', 'id':'entry-price', 'required':False}),
            'entry_amount': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Entry Amount (USD)'}),
        }
    
    def save(self, commit=True):
        instance = super(HoldingForm, self).save(commit=False)
        _name = self.cleaned_data.get('name').split(' (')
        instance.coin_id = _name[0]
        instance.symbol = _name[1][:-1]
        instance.save()
        return instance
     
    def clean_entry_price(self):
        value = self.cleaned_data["entry_price"]
        if value == 0:
            raise forms.ValidationError("Entry Price cannot be 0 or negative")
        elif not value:
            value = 1
        return value



