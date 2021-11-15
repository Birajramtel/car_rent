from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_OPTION = (('c', 'Credit Card'), ('d', 'Cash on Delivery'))


class PaymentForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField(blank_label='select country').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'}))
    order_notes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTION)


class ShippingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField(blank_label='select country').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'}))
    order_notes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))