from django import forms


class PaymentConfirmationForm(forms.Form):
    cardholder_name = forms.CharField(
        label="Nombre del Titular de la Tarjeta",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Titular de la Tarjeta'})
    )
    card_number = forms.CharField(
        label="Número de Tarjeta",
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Tarjeta'})
    )
    expiration_date = forms.CharField(
        label="Fecha de Expiración",
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        label="CVV",
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )