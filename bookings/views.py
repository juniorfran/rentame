from decimal import Decimal
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from users.models import Renter
from vehicles.models import Seguro
from .models import Booking, Vehicle, Descuento
from datetime import date, timedelta
from django.contrib import messages


def calcular_precio(vehicle, start_date, end_date, descuento, seguro):
    # Lógica para calcular el precio de la reserva
    precio_base = Decimal(str(vehicle.price_daily))  # Convierte el precio diario a Decimal
    seguro = Seguro.objects.filter(id=id)

    # Calcula la duración de la reserva
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    duracion = (end_date - start_date).days

    # Obtiene la instancia de Descuento
    descuento_instancia = Descuento.objects.get(codigo=descuento)  # Asume que descuento es el código del descuento

    # Aplica el descuento si es válido
    descuento_porcentaje = descuento_instancia.porcentaje_descuento
    precio_con_descuento = precio_base * (1 - descuento_porcentaje / 100)
    

    # Calcula el precio total con el seguro
    precio_total = precio_con_descuento * duracion
    precio_total = Decimal(str(precio_total))
    if seguro == 'seguro1':
        precio_total += Decimal('50')  # Utiliza Decimal para representar el seguro

    return precio_total

def reserva(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    # Obtén la lista de seguros disponibles desde la base de datos
    seguros_disponibles = Seguro.objects.all()
    # Obtener las fechas de reserva del vehículo
    reservas = Booking.objects.filter(vehicle=vehicle)
    # Crear una lista de fechas no disponibles
    fechas_no_disponibles = []
    for reserva in reservas:
        fechas_no_disponibles.extend(
            [reserva.start_date.date() + timedelta(days=x) for x in range((reserva.end_date.date() - reserva.start_date.date()).days + 1)]
        )
    # Crear una lista de fechas disponibles
    fechas_disponibles = []
    # Fecha de inicio y finalización para buscar disponibilidad
    fecha_inicio_disponibilidad = date.today()  # Puedes ajustar esto a la fecha que desees
    fecha_finalizacion_disponibilidad = fecha_inicio_disponibilidad + timedelta(days=30)  # Ajusta la duración deseada
    # Generar un rango de fechas desde la fecha de inicio hasta la fecha de finalización
    rango_fechas_disponibilidad = [fecha_inicio_disponibilidad + timedelta(days=x) for x in range((fecha_finalizacion_disponibilidad - fecha_inicio_disponibilidad).days + 1)]
    # Verificar si cada fecha en el rango está disponible
    for fecha in rango_fechas_disponibilidad:
        fecha_disponible = True
        for reserva in reservas:
            if fecha >= reserva.start_date.date() and fecha <= reserva.end_date.date():
                fecha_disponible = False
                break
        if fecha_disponible:
            fechas_disponibles.append(fecha)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        fecha_inicio_seleccionada = date.fromisoformat(start_date)
        fecha_finalizacion_seleccionada = date.fromisoformat(end_date)

        # Verifica si alguna fecha seleccionada no está disponible
        if any(fecha_inicio_seleccionada <= fecha <= fecha_finalizacion_seleccionada for fecha in fechas_no_disponibles):
            messages.error(request, 'El vehículo no está disponible en esas fechas.')
            return redirect('create_reserva', vehicle_id=vehicle.id)
        descuento = request.POST.get('descuento')
        seguro_id = request.POST.get('seguro')  # Obtén el ID del seguro
        # Calcula el precio de la reserva
        precio = calcular_precio(vehicle, start_date, end_date, descuento, seguro_id)  # Pasa el ID del seguro en lugar de la cadena
        renter, created = Renter.objects.get_or_create(user=request.user)
        # Obtén la instancia de Descuento basada en el valor proporcionado (código de descuento, por ejemplo)
        try:
            descuento_instancia = Descuento.objects.get(codigo=descuento)
        except Descuento.DoesNotExist:
            # Maneja el caso en el que el descuento no se encuentra
            raise ValueError("Descuento no encontrado")

        # Obtén la instancia de Seguro basada en el ID proporcionado
        try:
            seguro_instancia = Seguro.objects.get(id=seguro_id)
        except Seguro.DoesNotExist:
            # Maneja el caso en el que el seguro no se encuentra
            raise ValueError("Seguro no encontrado")
        # Crea la reserva y asigna el descuento y el seguro
        reserva = Booking(
            vehicle=vehicle,
            renter=renter,
            start_date=start_date,
            end_date=end_date,
            descuento=descuento_instancia,
            seguro=seguro_instancia,
            precio=precio,  # Asigna el precio al crear la reserva
        )
        reserva.save()
        messages.success(request, 'Reserva exitosa.')
        return redirect('detail_booking', reserva.id)
    
    fechas_disponibles = [date.strftime('%Y/%m/%d') for date in fechas_disponibles]
    fechas_disponibles_json = json.dumps(fechas_disponibles)
    fechas_no_disponibles = [date.strftime('%Y/%m/%d') for date in fechas_no_disponibles]
    fechas_no_disponibles_json = json.dumps(fechas_no_disponibles)
    
    context = {
        'vehicle': vehicle,
        'fechas_no_disponibles': fechas_no_disponibles,
        'fechas_no_disponibles_json': fechas_no_disponibles_json,
        'fechas_disponibles_json': fechas_disponibles_json,
        'seguros_disponibles': seguros_disponibles,
    }
    return render(request, 'booking/create_booking.html', context)


def detail_booking(request, reserva_id):
    # Recupera la reserva de la base de datos o muestra un error 404 si no existe
    reserva = get_object_or_404(Booking, id=reserva_id)

    return render(request, 'booking/detail_booking.html', {'reserva': reserva})