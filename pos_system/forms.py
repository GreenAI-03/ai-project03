from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=300)
    payment_method = forms.CharField(max_length=100)
