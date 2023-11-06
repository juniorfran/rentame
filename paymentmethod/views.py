# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import CreditCardPayment
from .forms import CreditCardPaymentForm
from django.contrib.auth.decorators import login_required

def lista_credit_card_payments(request):
    credit_card_payments = CreditCardPayment.objects.filter(user=request.user)
    return render(request, 'list.html', {'credit_card_payments': credit_card_payments})

@login_required  # Asegúrate de que el usuario esté autenticado
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
