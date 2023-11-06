# forms.py
from django import forms

from users.models import User
from .models import CreditCardPayment


class CreditCardPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditCardPayment
        exclude = ['user']  # Excluye el campo 'user' del formulario

    def __init__(self, *args, **kwargs):
        super(CreditCardPaymentForm, self).__init__(*args, **kwargs)
        # Establece el usuario automáticamente
        self.instance.user = kwargs.get('initial', {}).get('user')

        # Agrega el campo oculto para el usuario
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.filter(id=self.instance.user.id),
            widget=forms.HiddenInput(),
        )