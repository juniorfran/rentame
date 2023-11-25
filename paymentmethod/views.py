# views.py
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import CreditCardPayment, BankTransferPayment, PaymentMethod
from users.models import VehicleOwner
from transactions.models import Transaction
from .forms import CreditCardPaymentForm, BankTransferPaymentForm
from django.contrib.auth.decorators import login_required

## VISTA METODOS DE PAGO GENERAL

@login_required
def lista_payment_method(request):
    user = request.user
    #payment_methods = PaymentMethod.objects.filter(user=user)
    credit_card_payments = CreditCardPayment.objects.filter(user=user)
    payment_methods = PaymentMethod.objects.all()
    # credit_card_payments = CreditCardPayment.objects.all()
    
    context = {
        'payment_methods': payment_methods,
        'credit_card_payments': credit_card_payments
    }
    
    return render(request, 'list.html', context)


## VISTA CRUD METODO DE PAGO (TARJETA DE CREDITO)

@login_required
def list_creditcard_payment(request):
    credit_card_payments = CreditCardPayment.objects.all()
        
    return render(request, 'creditcard/listmethod.html', {'credit_card_payments': credit_card_payments})

@login_required
def add_creditcard_payment(request):
    if request.method == 'POST':
        form = CreditCardPaymentForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            credit_card_payment = form.save(commit=False)
            credit_card_payment.user = request.user
            credit_card_payment.save()
            return redirect('list_payments')  # Reemplaza 'perfil' con la URL de destino adecuada
    else:
        form = CreditCardPaymentForm(initial={'user': request.user})
    return render(request, 'creditcard/createmethod.html', {'form': form})
@login_required
def edit_creditcard_payment(request, pk):
    credit_card_payment = get_object_or_404(CreditCardPayment, id=pk)
    credit_card_payment.user = request.user  # Asignar el usuario al objeto CreditCardPayment
    if request.method == 'POST':
        form = CreditCardPaymentForm(request.POST, instance=credit_card_payment)
        if form.is_valid():
            credit_card_payment = form.save(commit=False)
            credit_card_payment.save()
            return redirect('list_payments')
    else:
        form = CreditCardPaymentForm(instance=credit_card_payment)
    return render(request, 'creditcard/editmethod.html', {'form': form})

@login_required
def delete_creditcard_payment(request, pk):
    credit_card_payment = get_object_or_404(CreditCardPayment, id=pk)
    if request.method == 'POST':
        credit_card_payment.delete()
        return redirect('list_payments')
    return render(request, 'creditcard/delete_creditcard_payment.html', {'credit_card_payment': credit_card_payment})



## VISTA CRUD METODO DE PAGO (TRANSFERENCIA BANCARIA)
@login_required
def add_bank_transfer_payment(request):
    if request.method == 'POST':
        form = BankTransferPaymentForm(request.POST)
        if form.is_valid():
            bank_transfer_payment = form.save(commit=False)
            bank_transfer_payment.user = request.user
            bank_transfer_payment.save()
            return redirect('list_payments')
    else:
        form = BankTransferPaymentForm()
    return render(request, 'banktransfer/add_bank_transfer_payment.html', {'form': form})

@login_required
def edit_bank_transfer_payment(request, pk):
    bank_transfer_payment = get_object_or_404(BankTransferPayment, pk=pk)
    if request.method == 'POST':
        form = BankTransferPaymentForm(request.POST, instance=bank_transfer_payment)
        if form.is_valid():
            bank_transfer_payment = form.save(commit=False)
            bank_transfer_payment.user = request.user
            bank_transfer_payment.save()
            return redirect('list_payments')
    else:
        form = BankTransferPaymentForm(instance=bank_transfer_payment)
    return render(request, 'banktransfer/edit_bank_transfer_payment.html', {'form': form})

@login_required
def delete_bank_transfer_payment(request, pk):
    bank_transfer_payment = get_object_or_404(BankTransferPayment, pk=pk)
    if request.method == 'POST':
        bank_transfer_payment.delete()
        return redirect('list_payments')
    return render(request, 'banktransfer/delete_bank_transfer_payment.html', {'bank_transfer_payment': bank_transfer_payment})



# ## VISTAS PARA CREAR METODO DE PAGO
# @login_required(login_url='/accounts/signup')
# def create_payment_methodCreditcard(request):
#     if request.method == 'POST':
#         type_method_id = request.POST.get('type_method')
#         cardholder_name = request.POST.get('cardholder_name')
#         card_number = request.POST.get('card_number')
#         expiration_date_mm_yy = request.POST.get('expiration_date')
#         cvv = request.POST.get('cvv')
#         transaction_id = request.POST.get('transaction')

#         try:
#             type_method_id = int(request.POST.get('type_method'))
#             type_method = PaymentMethod.objects.get(id=type_method_id)

#             try:
#                 transaction_id = int(request.POST.get('transaction'))
#                 transaction = Transaction.objects.get(id=transaction_id)
#             except (ValueError, Transaction.DoesNotExist):
#                 transaction = None

#             if request.user.is_owner:
#                 # Convertir el formato de fecha MM/YY a YYYY-MM-DD
#                 expiration_date = datetime.strptime(expiration_date_mm_yy, '%m/%y')
#                 expiration_date = expiration_date.replace(day=1)  # Establecer el día en 1
                
#                 method_credit = CreditCardPayment(
#                     user=request.user,
#                     typemethod=type_method,
#                     cardholder_name=cardholder_name,
#                     card_number=card_number,
#                     expiration_date=expiration_date,
#                     cvv=cvv,
#                     transaction=transaction
#                 )
#                 method_credit.save()
#                 return redirect('perfil')
#             else:
#                 return redirect('become_owner')
#         except (ValueError, PaymentMethod.DoesNotExist):
#             return redirect('lista_credit_card_payments')  # Otra acción adecuada según tus necesidades
#     else:
#         payment_methods = PaymentMethod.objects.all()
#         return render(request, 'creditcard/createmethod.html', {'payment_methods': payment_methods})

def method_estatus(request, paymentmethod_id):
    payment_method = get_object_or_404(PaymentMethod, id=paymentmethod_id)
    if request.method == 'POST':
        paymentmethod_id = request.POST.get('paymentmethod_id')
        if paymentmethod_id == str(payment_method.id):
            if payment_method.is_active:
                payment_method.is_active = False
            else:
                payment_method.is_active = True
            
            payment_method.save()
            return render(request,'creditcard/estatus_method.html', {'payment_method':payment_method})
        
    return render(request, 'creditcard/estatus_method.html', {'payment_method':payment_method})



