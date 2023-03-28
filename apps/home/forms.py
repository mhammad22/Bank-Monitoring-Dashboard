from django import forms

from apps.home.db import BankNamesChoices

class AddBankForm(forms.Form):
    
    input_attr = {'class': 'form-control'}
    
    username = forms.CharField(max_length=40, min_length=0, required=True)
    username.widget.attrs.update(input_attr)
    password = forms.CharField(max_length=20, min_length=0, required=True)
    password.widget.attrs.update(input_attr)
    url = forms.CharField(max_length=20, min_length=0, required=True)
    url.widget.attrs.update(input_attr)
    name = forms.ChoiceField(choices=BankNamesChoices, required=True)
    name.widget.attrs.update(input_attr)
    acc_num = forms.DecimalField(max_digits=20, decimal_places=4, required=True)
    acc_num.widget.attrs.update(input_attr)
    
class RefreshTimeForm(forms.Form):
    
    input_attr = {'class': 'form-control'}
    
    time = forms.IntegerField(required=True)
    time.widget.attrs.update(input_attr)