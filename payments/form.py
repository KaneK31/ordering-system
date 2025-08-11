from django import forms


class CheckoutAddressForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    address1 = forms.CharField(max_length=200, label="Address line 1")
    address2 = forms.CharField(max_length=200, required=False, label="Address line 2")
    city = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=30, required=False)
