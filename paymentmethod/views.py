# views.py
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import CreditCardPayment, BankTransferPayment, PaymentMethod
from users.models import VehicleOwner
from transactions.models import Transaction
from .forms import CreditCardPaymentForm
from django.contrib.auth.decorators import login_required


## VISTAS PARA CREAR METODO DE PAGO
@login_required(login_url='/accounts/signup')
def create_payment_methodCredit(request):
    if request.method == 'POST':
        type_method_id = request.POST.get('type_method')
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiration_date_mm_yy = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')
        transaction_id = request.POST.get('transaction')

        try:
            type_method_id = int(request.POST.get('type_method'))
            type_method = PaymentMethod.objects.get(id=type_method_id)

            try:
                transaction_id = int(request.POST.get('transaction'))
                transaction = Transaction.objects.get(id=transaction_id)
            except (ValueError, Transaction.DoesNotExist):
                transaction = None

            if request.user.is_owner:
                # Convertir el formato de fecha MM/YY a YYYY-MM-DD
                expiration_date = datetime.strptime(expiration_date_mm_yy, '%m/%y')
                expiration_date = expiration_date.replace(day=1)  # Establecer el día en 1
                
                method_credit = CreditCardPayment(
                    user=request.user,
                    typemethod=type_method,
                    cardholder_name=cardholder_name,
                    card_number=card_number,
                    expiration_date=expiration_date,
                    cvv=cvv,
                    transaction=transaction
                )
                method_credit.save()
                return redirect('perfil')
            else:
                return redirect('become_owner')
        except (ValueError, PaymentMethod.DoesNotExist):
            return redirect('lista_credit_card_payments')  # Otra acción adecuada según tus necesidades
    else:
        payment_methods = PaymentMethod.objects.all()
        return render(request, 'creditcard/createmethod.html', {'payment_methods': payment_methods})

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



def lista_credit_card_payments(request):
    credit_card_payments = CreditCardPayment.objects.filter(user=request.user)
    return render(request, 'list.html', {'credit_card_payments': credit_card_payments})

@login_required
def crear_credit_card_payment(request):
    if request.method == 'POST':
        form = CreditCardPaymentForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('lista_credit_card_payments')
    else:
        form = CreditCardPaymentForm(initial={'user': request.user})

    return render(request, 'create.html', {'form': form})

def editar_credit_card_payment(request, payment_id):
    payment = get_object_or_404(CreditCardPayment, id=payment_id, user=request.user)
    if request.method == 'POST':
        form = CreditCardPaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('lista_credit_card_payments')
    else:
        form = CreditCardPaymentForm(instance=payment)
    return render(request, 'edit.html', {'form': form, 'payment': payment})

def deshabilitar_credit_card_payment(request, payment_id):
    payment = get_object_or_404(CreditCardPayment, id=payment_id, user=request.user)
    if request.method == 'POST':
        payment.delete()
        return JsonResponse({'message': 'Pago deshabilitado con éxito.'})
    return JsonResponse({'message': 'Error al deshabilitar el pago.'})
