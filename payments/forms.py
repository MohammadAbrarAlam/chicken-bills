from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label="Amount (₹)", min_value=0.01, decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter amount'}))
