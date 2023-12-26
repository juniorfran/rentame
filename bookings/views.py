import datetime
import requests
from decimal import Decimal
from dateutil.parser import parse
from django.utils import timezone
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from bookings.forms import PaymentConfirmationForm
from paymentmethod.models import CreditCardPayment, PaymentMethod
from transactions.models import Transaction
from users.models import Renter, UserProfile, User, VehicleOwner
from vehicles.models import Seguro
from .models import Booking, Vehicle, Descuento
#from vehicles.models import Booking
from datetime import date, timedelta
from django.contrib import messages
from django.db import transaction as db_transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Función para calcular el precio total de la reserva
def calcular_precio_total(start_date, end_date, vehicle, descuento_codigo=None, seguro_id=None):
    
    dias_reserva = (end_date - start_date).days
    precio_por_dia = vehicle.price_daily
    precio_base = precio_por_dia * dias_reserva

    descuento_aplicado = 0
    if descuento_codigo:
        try:
            descuento = Descuento.objects.get(codigo=descuento_codigo)
            if descuento.fecha_inicio <= start_date and descuento.fecha_fin >= end_date:
                descuento_aplicado = precio_base * descuento.porcentaje_descuento / 100
        except Descuento.DoesNotExist:
            pass

    precio_con_descuento = precio_base - descuento_aplicado

    costo_seguro = 0
    if seguro_id:
        try:
            seguro = Seguro.objects.get(id=seguro_id)
            costo_seguro = seguro.costo_diario * dias_reserva
        except Seguro.DoesNotExist:
            pass

    precio_total = precio_con_descuento + costo_seguro
    return precio_total


def reserva(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    #renter, created = Renter.objects.get_or_create(user=request.user)
    user = request.user
    profile = UserProfile.objects.get(user=request.user)
    vehicle_owner = VehicleOwner.objects.get(user=user)
    seguros_disponibles = Seguro.objects.all()
    reservas = Booking.objects.filter(vehicle=vehicle)
    metodos_pago_disponibles = PaymentMethod.objects.all()
    
    try:
        renter = Renter.objects.get(user=request.user)
    except Renter.DoesNotExist:
        # Redirige al usuario a la URL 'create_renter/' para crear el perfil de Renter
        return redirect('create_renter')
    
    fechas_no_disponibles = []
    for reserva in reservas:
        fechas_no_disponibles.extend(
            [reserva.start_date.date() + timedelta(days=x) for x in range((reserva.end_date.date() - reserva.start_date.date()).days + 1)]
        )

    fechas_disponibles = []
    fecha_inicio_disponibilidad = date.today()
    fecha_finalizacion_disponibilidad = fecha_inicio_disponibilidad + timedelta(days=30)
    rango_fechas_disponibilidad = [fecha_inicio_disponibilidad + timedelta(days=x) for x in range((fecha_finalizacion_disponibilidad - fecha_inicio_disponibilidad).days + 1)]
    for fecha in rango_fechas_disponibilidad:
        fecha_disponible = True
        for reserva in reservas:
            if fecha >= reserva.start_date.date() and fecha <= reserva.end_date.date():
                fecha_disponible = False
                break
        if fecha_disponible:
            fechas_disponibles.append(fecha)

    if request.method == 'POST':
        start_date_iso = request.POST.get('start_date')
        end_date_iso = request.POST.get('end_date')
        descuento_id = request.POST.get('descuento_id')
        seguro_id = request.POST.get('seguro_id')
        metodo_pago_id = request.POST.get('metodo_pago_id')
        
        # Convert the ISO format strings to datetime objects
        start_date = parse(start_date_iso)
        end_date = parse(end_date_iso)

        # Make them timezone aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        
        metodo_pago_seleccionado = get_object_or_404(PaymentMethod, pk=metodo_pago_id)
        
        try:
            descuento_instancia = Descuento.objects.get(id=descuento_id)
        except Descuento.DoesNotExist:
            descuento_instancia = None

        try:
            seguro_instancia = Seguro.objects.get(id=seguro_id)
        except Seguro.DoesNotExist:
            seguro_instancia = None

        precio_total = calcular_precio_total(start_date, end_date, vehicle, descuento_id, seguro_id=None)

        reserva = Booking(
            vehicle=vehicle,
            renter=renter,
            start_date=start_date,
            end_date=end_date,
            descuento=descuento_instancia,
            seguro=seguro_instancia,
            precio=precio_total,
            paymentmethod=metodo_pago_seleccionado
        )
        reserva.save()

        transaction = Transaction.objects.create(
            renter=renter,
            vehicle=vehicle,
            amount=precio_total,
            create_add=date.today(),
        )
        transaction.save()
        
        #renter.bookings.add(reserva.id)
        vehicle_owner.rented_vehicles.add(vehicle)

        messages.success(request, 'Reserva exitosa.')

        # Crear el enlace de pago utilizando la información de la reserva
        enlace_pago = crear_enlace_pago(vehicle, renter, start_date, end_date, precio_total)

        if "url_enlace_pago" in enlace_pago:
            # Almacenar los datos del enlace de pago en la reserva
            reserva.url_enlace = enlace_pago["url_enlace_pago"]
            reserva.url_qr_code_enlace = enlace_pago["url_qr_code_enlace"]
            reserva.id_enlace = enlace_pago["id_enlace"]
            reserva.esta_productivo = enlace_pago["esta_productivo"]
            reserva.save()

            # Imprimir para verificar que los datos se almacenan correctamente
            print(f"ID del enlace: {reserva.id_enlace}")
            print(f"URL del QR: {reserva.url_qr_code_enlace}")
            print(f"URL del enlace: {reserva.url_enlace}")
            print(f"¿Está productivo?: {reserva.esta_productivo}")

            # Puedes redirigir a la página de detalles de reserva o donde desees
            return redirect('detail_booking', reserva.id)
        else:
            # Manejar el caso de error y mostrar mensajes
            messages.error(request, enlace_pago.get("mensajes"))

    fechas_disponibles = [date.strftime('%Y/%m/%d') for date in fechas_disponibles]
    fechas_disponibles_json = json.dumps(fechas_disponibles)
    fechas_no_disponibles = [date.strftime('%Y/%m/%d') for date in fechas_no_disponibles]
    fechas_no_disponibles_json = json.dumps(fechas_no_disponibles)
    
    tiene_metodos_pago = CreditCardPayment.objects.filter(user=request.user).exists()

    context = {
        'vehicle': vehicle,
        'fechas_no_disponibles': fechas_no_disponibles,
        'fechas_no_disponibles_json': fechas_no_disponibles_json,
        'fechas_disponibles_json': fechas_disponibles_json,
        'seguros_disponibles': seguros_disponibles,
        'user': user,
        'profile': profile,
        'vehicle_owner': vehicle_owner,
        'metodos_pago_disponibles': metodos_pago_disponibles,
        'renter': renter,
        'tiene_metodos_pago': tiene_metodos_pago
    }
    return render(request, 'booking/create_booking.html', context)


def detail_booking(request, reserva_id):
    # Recupera la reserva de la base de datos o muestra un error 404 si no existe
    # booking = Booking.objects.get(id=booking_id)
    reserva = get_object_or_404(Booking, id=reserva_id)
    
    context = {
        # 'booking': booking,
        'reserva': reserva
    }

    return render(request, 'booking/detail_booking.html', context)

## FUNCIONES Y VISTAS PARA REALIZAR PAGOS
def obtener_token_de_acceso():
    # Credenciales de la aplicación Wompi
    app_id = '50163375-39c0-4dc7-8d8b-b1bc34f6e419'
    api_secret = '2c68b6a6-9b41-42c7-b418-8315913bd006'

    # URL de Wompi para obtener el token de acceso
    token_url = 'https://id.wompi.sv/connect/token'

    # Parámetros del POST para la autenticación
    payload = {
        'grant_type': 'client_credentials',
        'audience': 'wompi_api',
        'client_id': app_id,
        'client_secret': api_secret
    }

    try:
        # Utilizar requests.post para realizar la solicitud POST
        response = requests.post(token_url, data=payload)

        if response.status_code == 200:
            # Si la solicitud es exitosa, obtener el token de acceso
            access_token = response.json().get('access_token')
            return access_token
        else:
            print(f"Error al obtener el token de acceso. Código de estado: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud para obtener el token de acceso: {e}")
        return None
    
def crear_enlace_pago(vehicle, renter, start_date, end_date, precio_total):
    try:
        # Obtener el token de acceso
        access_token = obtener_token_de_acceso()

        if access_token:
            # Obtener las imágenes del vehículo
            imagenes_vehiculo = vehicle.image.all()

            # Tomar solo la primera imagen si hay alguna
            imagen_vehiculo = imagenes_vehiculo.first() if imagenes_vehiculo else None

            # Verificar y construir la URL de la imagen del producto
            url_imagen_producto = imagen_vehiculo.image.url if imagen_vehiculo else None
            # Verifica que la URL tenga el formato correcto
            if url_imagen_producto and not url_imagen_producto.startswith(("http://", "https://")):
                url_imagen_producto = None

            # Convertir Decimal a float o str para serialización JSON
            precio_total_serializable = float(precio_total)  # O str(precio_total) según tus necesidades

            # Construir la URL de creación de enlace de pago
            url_creacion_enlace = 'https://api.wompi.sv/EnlacePago'

            # Construir el cuerpo de la solicitud
            body = {
                "identificadorEnlaceComercio": f"reserva_{vehicle.id}_{renter.id}_{int(datetime.timestamp(datetime.now()))}",
                "monto": precio_total_serializable,
                "nombreProducto": vehicle.make,  # Ajusta esto según la estructura de tu modelo Vehicle
                "formaPago": {
                    "permitirTarjetaCreditoDebido": True,
                    "permitirPagoConPuntoAgricola": True,
                    "permitirPagoEnCuotasAgricola": False
                },
                "infoProducto": {
                    "descripcionProducto": f"Reserva de {vehicle.make} del {start_date} al {end_date}",
                    "urlImagenProducto": url_imagen_producto
                },
                "configuracion": {
                    "urlRedirect": "https://rentamesv",  # URL a la que se redirige después de realizar el pago
                    "esMontoEditable": False,
                    "esCantidadEditable": False,
                    "emailsNotificacion": "correo@ejemplo.com",
                }
            }

            # Convertir el cuerpo a formato JSON
            body_json = json.dumps(body)

            # Encabezados de la solicitud
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            # Realizar la solicitud POST para crear el enlace de pago
            response = requests.post(url_creacion_enlace, data=body_json, headers=headers)

            if response.status_code == 200:
                # Si la solicitud es exitosa, obtener los datos relevantes
                enlace_pago_data = response.json()
                url_enlace_pago = enlace_pago_data.get('urlEnlace')
                url_qr_code_enlace = enlace_pago_data.get('urlQrCodeEnlace')
                id_enlace = enlace_pago_data.get('idEnlace')
                esta_productivo = enlace_pago_data.get('estaProductivo')

                return {
                    "url_enlace_pago": url_enlace_pago,
                    "url_qr_code_enlace": url_qr_code_enlace,
                    "id_enlace": id_enlace,
                    "esta_productivo": esta_productivo
                }
            else:
                # Manejar el caso de error en la respuesta
                error_response = response.json()
                raise Exception(error_response)

        else:
            # Si no se puede obtener el token de acceso
            raise Exception("Error al obtener el token de acceso.")

    except Exception as e:
        # Capturar excepciones y devolver un objeto estructurado con información sobre el error
        return {
            "servicioError": "Error al generar el enlace de pago",
            "mensajes": [str(e)],
            "subTipoError": "Error en la solicitud de Wompi"
        }
        
def listar_enlaces_pago(access_token):
    # URL para listar los enlaces de pago
    url_listar_enlaces = 'https://api.wompi.sv/EnlacePago'

    # Encabezados de la solicitud
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        # Realizar la solicitud GET para obtener la lista de enlaces de pago
        response = requests.get(url_listar_enlaces, headers=headers)

        if response.status_code == 200:
            # Si la solicitud es exitosa, obtener la lista de enlaces de pago
            enlaces_pago = response.json()
            return enlaces_pago
        else:
            print(f"Error al listar los enlaces de pago. Código de estado: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud para listar los enlaces de pago: {e}")
        return None
    
    
    
def listar_enlaces_pago_view(request):
    # Obtener el token de acceso
    access_token = obtener_token_de_acceso()

    if access_token:
        # Obtener la lista de enlaces de pago
        enlaces_pago = listar_enlaces_pago(access_token)

        if enlaces_pago:
            # Construir una cadena con la lista de enlaces de pago
            lista_enlaces_str = '\n'.join(str(enlace) for enlace in enlaces_pago)
            # Crear una respuesta HTTP con la lista de enlaces
            response = HttpResponse(lista_enlaces_str, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="enlaces_pago.txt"'
            return response
        else:
            mensaje_error = "No se pudo obtener la lista de enlaces de pago."
    else:
        mensaje_error = "No se pudo obtener el token de acceso."

    # Crear una respuesta HTTP con el mensaje de error
    response = HttpResponse(mensaje_error, content_type='text/plain')
    return response


# def realizar_transaccion_compra_3ds(access_token, numero_tarjeta, cvv, mes_vencimiento, anio_vencimiento, monto, url_redirect, nombre, apellido, email, ciudad, direccion, id_pais, id_region, codigo_postal, telefono):
#     url_transaccion_compra_3ds = "https://api.wompi.sv/TransaccionCompra/3Ds"

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     datos_transaccion = {
#         "tarjetaCreditoDebido": {
#             "numeroTarjeta": numero_tarjeta,
#             "cvv": cvv,
#             "mesVencimiento": mes_vencimiento,
#             "anioVencimiento": anio_vencimiento
#         },
#         "monto": monto,
#         "urlRedirect": url_redirect,
#         "nombre": nombre,
#         "apellido": apellido,
#         "email": email,
#         "ciudad": ciudad,
#         "direccion": direccion,
#         "idPais": id_pais,
#         "idRegion": id_region,
#         "codigoPostal": codigo_postal,
#         "telefono": telefono
#     }

#     try:
#         response = requests.post(url_transaccion_compra_3ds, json=datos_transaccion, headers=headers)

#         if response.status_code == 200:
#             respuesta_transaccion = response.json()
#             return respuesta_transaccion
#         else:
#             print(f"Error en la solicitud para realizar la transacción de compra 3DS. Código de estado: {response.status_code}")
#             return {"error": f"Error en la solicitud. Código de estado: {response.status_code}"}

#     except requests.exceptions.RequestException as e:
#         print(f"Error en la solicitud para realizar la transacción de compra 3DS: {e}")
#         return {"error": f"Error en la solicitud: {e}"}


# @login_required
# def procesar_transaccion_compra_3ds(request):
#     try:
#         # Obtener el perfil del usuario actual
#         user_profile = UserProfile.objects.get(user=request.user)

#         # Simulación de obtención del token de acceso (reemplaza con tu lógica real)
#         token_acceso = obtener_token_de_acceso()

#         if not token_acceso:
#             return HttpResponse('Error al obtener el token de acceso')

#         # Obtener datos de la reserva (ajusta según tus modelos y lógica)
#         reservation_id = request.POST.get('reservation_id')
#         metodo_pago_id = request.POST.get('metodo_pago_id')

#         # Obtener la reserva y el método de pago seleccionado
#         reserva = get_object_or_404(Booking, pk=reservation_id)
#         vehicle = reserva.vehicle
#         metodo_pago_seleccionado = get_object_or_404(PaymentMethod, pk=metodo_pago_id)

#         # Datos para el formulario
#         datos_real_reserva = {
#             'numero_tarjeta': metodo_pago_seleccionado.card_number,
#             'cvv': metodo_pago_seleccionado.cvv,
#             'mes_vencimiento': metodo_pago_seleccionado.mes_expiracion,
#             'anio_vencimiento': metodo_pago_seleccionado.anio_expiracion,
#             'monto': reserva.precio,  # Ajusta según tu modelo de reserva
#             'url_redirect': 'http://127.0.0.1:8000/booking/detalles_pago/',  # Ajusta la URL de redirección
#             'nombre': user_profile.nombre,
#             'apellido': user_profile.apellido,
#             'email': user_profile.user.email,
#             'ciudad': user_profile.ciudad,
#             'direccion': user_profile.direccion,
#             'id_pais': 'SV',
#             'id_region': 'SS',
#             'codigo_postal': '12345',
#             'telefono': user_profile.numero_telefono,
#         }

#         # Realizar la transacción de compra 3DS usando la función con datos reales
#         resultado_transaccion = realizar_transaccion_compra_3ds(access_token=token_acceso, **datos_real_reserva)

#         if "error" not in resultado_transaccion:
#             if resultado_transaccion.get("urlCompletarPago3Ds"):
#                 # Si hay una URL para completar el pago 3D Secure, redirige al usuario a esa URL
#                 return redirect(resultado_transaccion["urlCompletarPago3Ds"])
#             else:
#                 # Si no se requiere 3D Secure, puedes redirigir a la página de detalles del pago
#                 id_transaccion = resultado_transaccion.get("idTransaccion")

#                 # Actualizar el estado de la reserva a "Confirmada"
#                 reserva.estado = 'Confirmada'
#                 reserva.save()

#                 messages.success(request, 'Transacción de compra 3DS exitosa.')
#                 return render(request, 'booking/detail_booking.html', {'datos_real_reserva': datos_real_reserva})
#         else:
#             # Si el pago no se realiza, la reserva queda en estado "Pendiente"
#             reserva.estado = 'Pendiente'
#             reserva.save()

#             messages.error(request, f"Error al procesar la transacción de compra 3DS: {resultado_transaccion['error']}")
#             return redirect('detalle_reserva', reserva.id)

#     except Exception as e:
#         # Manejo de excepciones
#         messages.error(request, f"Error en el procesamiento de la transacción: {str(e)}")
#         return redirect('home')
    
    
    
# def detalles_transaccion(request, id_transaccion):
#     # Simulación de obtención del token de acceso (reemplaza con tu lógica real)
#     token_acceso = obtener_token_de_acceso()

#     if not token_acceso:
#         return HttpResponse('Error al obtener el token de acceso')

#     # URL de Wompi para obtener detalles de la transacción
#     url_detalles_transaccion = f'https://api.wompi.sv/TransaccionCompra/{id_transaccion}'

#     headers = {
#         'Authorization': f'Bearer {token_acceso}',
#         'Accept': 'text/plain',
#     }

#     try:
#         # Realizar la solicitud GET para obtener detalles de la transacción
#         response = requests.get(url_detalles_transaccion, headers=headers)

#         if response.status_code == 200:
#             detalles_transaccion = response.json()
#             return render(request, 'pagos/ver_detalles_pago.html', {'id_transaccion': id_transaccion, 'detalles_transaccion': detalles_transaccion})
#         else:
#             return HttpResponse(f"Error al obtener detalles de la transacción. Código de estado: {response.status_code}")

#     except requests.exceptions.RequestException as e:
#         return HttpResponse(f"Error en la solicitud para obtener detalles de la transacción: {e}")