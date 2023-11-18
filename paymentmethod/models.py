from django.db import models
from users.models import User  # Importa el modelo de usuario de Django si aún no lo has hecho
from transactions.models import Transaction  # Importa el modelo de transacción de tu aplicación de transacciones
from django.db.models.signals import pre_save
from django.dispatch import receiver

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    create_add = models.DateField(auto_now=False, auto_now_add=False,  null=True)

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"

    def __str__(self):
        return self.name

class CreditCardPayment(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='credit_card_user',
        null=True
    )
    typemethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    cardholder_name = models.CharField(max_length=100, verbose_name="Nombre del titular de la tarjeta")
    card_number = models.CharField(max_length=16, verbose_name="Número de tarjeta")
    # expiration_date = models.DateField(verbose_name="Fecha de expiración")
    # expiration_date = models.CharField(max_length=5, verbose_name="Fecha de expiración")
    mes_expiracion = models.CharField( max_length=5)
    anio_expiracion = models.CharField( max_length=5)
    cvv = models.CharField(max_length=4, verbose_name="CVV")
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='credit_card_payments',
        verbose_name="Transacción asociada",
        null=True
    )
    create_add = models.DateField(auto_now=False, auto_now_add=False,  null=True)
    
    

class PayPalPayment(models.Model):
    email = models.EmailField(max_length=100, verbose_name="Correo electrónico de PayPal")
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='paypal_payments',
        verbose_name="Transacción asociada"
    )
    create_add = models.DateField(auto_now=False, auto_now_add=False,  null=True)

    class Meta:
        verbose_name = "Pago con PayPal"
        verbose_name_plural = "Pagos con PayPal"

    def __str__(self):
        return self.email

class BankTransferPayment(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='bank_transfer_user',
        null=True
    )
    account_holder = models.CharField(max_length=100, verbose_name="Nombre del titular de la cuenta")
    account_number = models.CharField(max_length=20, verbose_name="Número de cuenta")
    bank_name = models.CharField(max_length=100, verbose_name="Nombre del banco")
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='bank_transfer_payments',
        verbose_name="Transacción asociada"
    )
    create_add = models.DateField(auto_now=False, auto_now_add=False,  null=True)

    class Meta:
        verbose_name = "Transferencia Bancaria"
        verbose_name_plural = "Transferencias Bancarias"

    def __str__(self):
        return self.account_holder
