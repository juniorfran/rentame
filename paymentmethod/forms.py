# forms.py
from django import forms
from django.utils import timezone
from users.models import User
from .models import CreditCardPayment, BankTransferPayment
import re

class CreditCardPaymentForm(forms.ModelForm):
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY', 'autocomplete': 'off'}),
        help_text='Formato: MM/YY',
    )

    class Meta:
        model = CreditCardPayment
        exclude = ['user', 'transaction', 'create_add']
        fields = [
            'typemethod',
            'cardholder_name',
            'card_number',
            'expiration_date',
            'cvv',
            'transaction',
        ]
        widgets = {
            'typemethod': forms.Select(attrs={'class': 'form-select', 'autocomplete': 'off'}),
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'transaction': forms.Select(attrs={'class': 'form-select', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreditCardPaymentForm, self).__init__(*args, **kwargs)
        self.instance.user = kwargs.get('initial', {}).get('user')
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.filter(id=self.instance.user.id),
            widget=forms.HiddenInput(),
        )

    def clean(self):
        cleaned_data = super().clean()
        expiration_date = cleaned_data.get('expiration_date', '')

        if not expiration_date or not re.match(r'^\d{2}/\d{2}$', expiration_date):
            self.add_error('expiration_date', 'Formato de fecha inválido. Use MM/YY.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.create_add = timezone.now()

        if commit:
            instance.save()

        return instance

    
## FORMULARIO DE TRANSFERENCIA BANCARIA
class BankTransferPaymentForm(forms.ModelForm):
    class Meta:
        model = BankTransferPayment
        exclude = ['user', 'transaction']  # Excluye el campo 'user' y 'transaction del formulario

    def __init__(self, *args, **kwargs):
        super(BankTransferPaymentForm, self).__init__(*args, **kwargs)
        # Establece el usuario automáticamente
        self.instance.user = kwargs.get('initial', {}).get('user')

        # Agrega el campo oculto para el usuario
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.filter(id=self.instance.user.id),
            widget=forms.HiddenInput(),
        )
        