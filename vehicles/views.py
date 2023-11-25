from decimal import ROUND_HALF_UP, Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from vehicles.models import Imagen, Vehicle, VehicleType, Location
from reviews.models import Review
from users.models import Renter, User, UserProfile, VehicleOwner
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import VehicleTypeForm, LocationForm

# Create your views here.
# @login_required
# def add_review(request, vehicle_id):
#     vehicle = Vehicle.objects.get(pk=vehicle_id)
    
#     # Verifica si el usuario tiene un perfil de "renter"
#     if not request.user.renter_profile:  # Supongamos que tienes un campo llamado "renter_profile" en tu modelo de usuario
#         # Si el usuario no tiene un perfil de "renter", redirige a la página de creación de perfil
#         return redirect('create_renter')  # Reemplaza 'crear_perfil_renter' con la URL real de creación de perfil
    
#     if request.method == 'POST':
#         # Procesar el formulario enviado en la plantilla
#         rating = request.POST.get('rating')
#         comment = request.POST.get('comment')
#         reviewed_by = request.user

#         review = Review(vehicle=vehicle, rating=rating, comment=comment, reviewed_by=reviewed_by)
#         review.save()

#         return redirect('vehicle_detail', vehicle_id=vehicle.id)

#     return render(request, 'review_create.html', {'vehicle': vehicle})
@login_required
def vehicledetail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    imagen = vehicle.image.all()
    reviews = vehicle.reviews_vehicle.all()

    # Verificar si el usuario tiene un perfil de Renter
    user_renter_profile = Renter.objects.filter(user=request.user).first()
    user_has_renter_profile = user_renter_profile is not None

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Verificar si el usuario tiene un perfil de Renter
        if user_renter_profile:
            # Si el usuario tiene un perfil de Renter, usa ese perfil como reviewed_by
            reviewed_by = user_renter_profile
        else:
            # Si el usuario no tiene un perfil de Renter, puedes manejarlo según tus necesidades.
            # Por ejemplo, puedes mostrar un mensaje de error o simplemente no asignar un reviewed_by.
            # Aquí, asignamos None.
            reviewed_by = None

        review = Review(vehicle=vehicle, rating=rating, comment=comment, reviewed_by=reviewed_by)
        review.save()

        return redirect('vehicle_detail', vehicle_id=vehicle.id)
    
    # Realiza los cálculos para aplicar el descuento
    precio_original = vehicle.price_daily
    descuento = precio_original * Decimal('0.20')
    precio_con_descuento = precio_original - descuento
    
    # Redondea el precio con descuento a dos decimales
    precio_con_descuento = precio_con_descuento.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    context = {
        'vehicle': vehicle,
        'imagen': imagen,
        'reviews': reviews,
        'user_has_renter_profile': user_has_renter_profile,
        'precio_con_descuento': precio_con_descuento,
    }

    return render(request, 'vehicle_detail.html', context)

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(availability=True).order_by('-id')  # Ordena la lista de vehículos por fecha de creación en orden descendente
    vehicle_types = VehicleType.objects.all()
    locations = Location.objects.all()
    
    paginator = Paginator(vehicles, 10)  # Configurar el paginador con 10 elementos por página
    page = request.GET.get('page')
    
    try:
        vehicles = paginator.page(page)  # Obtener la página específica
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página.
        vehicles = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por encima del número máximo de páginas), mostrar la última página.
        vehicles = paginator.page(paginator.num_pages)
    
    context = {
        'vehicles': vehicles,
        'vehicle_types': vehicle_types,
        'locations': locations
    }
    
    return render(request, 'vehicle_list.html', context)

@login_required
def crear_vehiculo(request):
    # Mueve la definición de las listas locations y vehicle_types aquí para que estén disponibles en el alcance de la vista
    locations = Location.objects.all()
    vehicle_types = VehicleType.objects.all()

    if request.method == 'POST':
        # Obtén los datos del formulario
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        anio = request.POST['anio']
        color = request.POST['color']
        puertas = request.POST['puertas']
        transmision = request.POST['transmision']
        cilindraje = request.POST['cilindraje']
        descripcion = request.POST['descripcion']
        precio_por_hora = request.POST['precio_por_hora']
        precio_por_dia = request.POST['precio_por_dia']
        disponibilidad = request.POST.get('disponibilidad')
        disponibilidad = disponibilidad == 'on'
        combustible = request.POST['combustible']
        motor = request.POST['motor']
        tipo_freno = request.POST['tipo_freno']
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        location = request.POST.get('ubicacion')

        # Obtén el usuario autenticado
        user = request.user

        if user.is_owner:
            try:
                # Intenta obtener el VehicleOwner relacionado con el User
                vehicle_owner, created = VehicleOwner.objects.get_or_create(user=user)

                # Intenta obtener el objeto VehicleType correspondiente al ID proporcionado
                vehicle_type = VehicleType.objects.get(id=tipo_vehiculo)
                location = Location.objects.get(id=location)

                # Si se encontró un VehicleOwner y un VehicleType válido, procede a crear el vehículo
                vehicle = Vehicle(owner=vehicle_owner, vehicle_type=vehicle_type, location=location)
                vehicle.make = marca
                vehicle.model = modelo
                vehicle.year = anio
                vehicle.color = color
                vehicle.puertas = puertas
                vehicle.transmision = transmision
                vehicle.cilindraje = cilindraje
                vehicle.description = descripcion
                vehicle.price_hourly = precio_por_hora
                vehicle.price_daily = precio_por_dia
                vehicle.availability = disponibilidad
                vehicle.combustible = combustible
                vehicle.motor = motor
                vehicle.tipo_freno = tipo_freno
                vehicle.save()

                # Procesa las imágenes
                imagenes = request.FILES.getlist('imagenes[]')
                for imagen in imagenes:
                    imagen_obj = Imagen(image=imagen, user=request.user)
                    imagen_obj.save()
                    vehicle.image.add(imagen_obj)
                    
                return redirect('vehicle_list')
            
            except VehicleType.DoesNotExist:
                # Si no se encontró un VehicleType correspondiente, muestra un mensaje de error
                Message.error(request, 'El tipo de vehículo seleccionado no es válido.')
                return redirect('become_owner')
        else:
            # Si el usuario no es propietario, redirige al usuario a la página de registro de propietario
            return redirect('become_owner')

    context = {
        'locations': locations,
        'vehicle_types': vehicle_types,
    }

    return render(request, 'user/vehicle_user_create.html', context)


@login_required
def crear_vehiculo_paso1(request):
    user = request.user
    
    if not hasattr(user, 'vehicle_owner_profile'):
        # El usuario no tiene un registro como VehicleOwner, redirigir a la vista para crear el perfil de propietario
        return redirect('complete_verification')
    
    if user.is_owner:
        if request.method == 'POST':
            marca = request.POST['marca']
            modelo = request.POST['modelo']
            anio = request.POST['anio']
            color = request.POST['color']
            puertas = request.POST['puertas']
            transmision = request.POST['transmision']
            cilindraje = request.POST['cilindraje']
            descripcion = request.POST['descripcion']

            datos_paso1 = {
                'marca': marca,
                'modelo': modelo,
                'anio': anio,
                'color': color,
                'puertas': puertas,
                'transmision': transmision,
                'cilindraje': cilindraje,
                'descripcion': descripcion,
            }

            request.session['datos_paso1'] = datos_paso1

            return redirect('crear_vehiculo_paso2')
    else:
        return redirect('complete_verification')
    
    return render(request, 'crear_vehiculo_paso1.html')

@login_required
def crear_vehiculo_paso2(request):
    if request.method == 'POST':
        precio_por_dia = request.POST['precio_por_dia']
        disponibilidad = request.POST.get('disponibilidad')
        combustible = request.POST['combustible']
        motor = request.POST['motor']
        climatizacion = request.POST['climatizacion']
        kilometraje = request.POST['kilometraje']
        tipo_freno = request.POST['tipo_freno']

        datos_paso1 = request.session.get('datos_paso1', {})

        datos_paso2 = {
            'precio_por_dia': precio_por_dia,
            'disponibilidad': disponibilidad == 'on',
            'combustible': combustible,
            'motor': motor,
            'tipo_freno': tipo_freno,
            'climatizacion': climatizacion,
            'kilometraje': kilometraje,
        }

        datos_combinados = {**datos_paso1, **datos_paso2}
        request.session['datos_combinados'] = datos_combinados

        return redirect('crear_vehiculo_paso3')

    return render(request, 'crear_vehiculo_paso2.html')

@login_required
def crear_vehiculo_paso3(request):
    locations = Location.objects.all()
    vehicle_types = VehicleType.objects.all()
    
    if request.method == 'POST':
        datos_combinados = request.session.get('datos_combinados', {})

        try:
            vehicle_owner = VehicleOwner.objects.get(user=request.user)
        except VehicleOwner.DoesNotExist:
            return redirect('complete_verification')

        vehicle = Vehicle(owner=vehicle_owner)
        vehicle.availability = datos_combinados.get('disponibilidad', False)
        vehicle.make = datos_combinados.get('marca', '')
        vehicle.model = datos_combinados.get('modelo', '')
        vehicle.year = datos_combinados.get('anio', 0)
        vehicle.cilindraje = datos_combinados.get('cilindraje', 0)
        vehicle.description = datos_combinados.get('descripcion', '')
        vehicle.price_hourly = datos_combinados.get('precio_por_hora', 0)
        vehicle.price_daily = datos_combinados.get('precio_por_dia', 0)
        vehicle.color = datos_combinados.get('color')
        vehicle.puertas = datos_combinados.get('puertas')
        vehicle.climatizacion = datos_combinados.get('climatizacion')
        vehicle.transmision = datos_combinados.get('transmision')
        vehicle.kilometraje = datos_combinados.get('kilometraje', 0)
        vehicle.combustible = datos_combinados.get('combustible')
        vehicle.motor = datos_combinados.get('motor')
        vehicle.tipo_freno = datos_combinados.get('tipo_freno')

        try:
            tipo_vehiculo_id = request.POST.get('tipo_vehiculo')
            location_id = request.POST.get('ubicacion')
            tarjeta_circulacion_1 = request.POST.get('tarjeta_circulacion1')
            tarjeta_circulacion_2 = request.POST.get('tarjeta_circulacion2')

            vehicle_type = vehicle_types.get(id=tipo_vehiculo_id)
            location = locations.get(id=location_id)

            vehicle.vehicle_type = vehicle_type
            vehicle.location = location
            vehicle.foto_tarjeta_circulacion_1 = tarjeta_circulacion_1
            vehicle.foto_tarjeta_circulacion_2 = tarjeta_circulacion_2
            
            vehicle.save()

            imagenes = request.FILES.getlist('imagenes[]')

            for imagen in imagenes:
                imagen_obj = Imagen(image=imagen, user=request.user)
                imagen_obj.save()
                vehicle.image.add(imagen_obj)

            return redirect('vehicle_list')
        except (VehicleType.DoesNotExist, Location.DoesNotExist):
            return redirect('complete_verification')

    return render(request, 'crear_vehiculo_paso3.html', {'locations': locations, 'vehicle_types': vehicle_types})



def vehicle_type_create(request):
    form = VehicleTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = VehicleTypeForm()
    context = {'form': form}
    return render(request, 'create_edit.html', context)

def vehicle_type_edit(request, pk):
    vehicle_type = VehicleType.objects.get(id=pk)
    form = VehicleTypeForm(request.POST or None, instance=vehicle_type)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(request, 'create_edit.html', context)

##vistas para ubicaciones del vehiculo
