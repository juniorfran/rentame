from multiprocessing import AuthenticationError
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
#from django.contrib.auth.models import User
from .models import UserProfile, VehicleOwner, Renter, User
from vehicles.models import Location, Vehicle, VehicleType
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserForm, UserProfileForm, VehicleOwnerForm, UserProfilCreateForm


# @login_required
# def update_profile(request):
#      # Verificar si el usuario ya tiene un perfil UserProfile
#     if not hasattr(request.user, 'profile'):
#         return redirect('crear_perfil')  # Redirige al usuario a la vista de creación de perfil

#     user_profile = request.user.profile
#     userform = UserForm(request.POST, instance=request.user)
#     userprofileform = UserProfileForm(request.POST, instance=request.user.user_profile)
#     vehicleownerform = VehicleOwnerForm(request.POST, request.FILES, instance=request.user.user_profile.vehicleowner)
     
#     if userform.is_valid() and userprofileform.is_valid() and vehicleownerform.is_valid():
#         userform.save()
#         userprofileform.save()
#         vehicleownerform.save()
#         messages.success(request, _('Your account has been updated successfully!'))
#         return redirect('perfil')
    
#     context = {
#         'userform': userform,
#         'userprofileform': userprofileform,
#         'vehicleownerform': vehicleownerform,
#     }
#     return render(request, 'perfil/editar_perfil.html', context)


#VISTA PARA VER EL PERFIL DEL USUARIO
@login_required
def profileView(request):
    user = request.user

    # Verificar si el usuario tiene un perfil
    if not UserProfile.objects.filter(user=user).exists():
        return redirect('crear_perfil')  # Redireccionar a la vista de creación de perfil

    # El usuario tiene un perfil, obtén los datos del perfil
    perfil = user.profile
    full_name = user.get_full_name()
    email = user.email
    vehicles = Vehicle.objects.filter(owner__user=user)

    context = {
        'perfil': perfil,
        'full_name': full_name,
        'email': email,
        'vehicles': vehicles,
    }

    return render(request, 'perfil/perfil.html', context)

#VISTA PARA REGISTRAR USUARIO SIN ARCHIVO FORM
# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
        
#         # Verifica si 'is_owner' está en la solicitud POST y es 'on', de lo contrario, establece False.
#         is_owner = request.POST.get('is_owner', False)
        
#         # Valida que las contraseñas coincidan
#         if password != confirm_password:
#             messages.error(request, 'Las contraseñas no coinciden.')
#             return redirect('register')

#         # Verifica si el usuario ya existe
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'El nombre de usuario ya está en uso.')
#             return redirect('register')

#         # Crea el nuevo usuario
#         user = User.objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password
#         )
#         user.is_owner = is_owner
#         user.save()
        
#         # Redirige al usuario al formulario de llenado de campos de VehicleOwner si es propietario
#         if is_owner:
#             return redirect('login')  # Cambia a la vista que muestra el formulario de VehicleOwner

#         messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
#         return redirect('login')

#     return render(request, 'users/register.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('perfil') # Reemplazar con la URL de la página principal
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# VISTA PARA REGISTRAR UN PERFIL
@login_required
def crear_perfil(request):
        # Verificar si el usuario ya tiene un perfil
    if UserProfile.objects.filter(user=request.user).exists():
        return redirect('perfil')

    if request.method == 'POST':
        # Obtén el usuario actualmente autenticado
        user = request.user
        email = request.user.email

        # Obtén los datos del formulario
        # email = request.POST['email']
        numero_telefono = request.POST['numero_telefono']
        direccion = request.POST['direccion']
        nombre = request.POST['nombre']
        imagen = request.FILES.get('imagen')  # campo de archivo para la imagen

        # Crea el objeto UserProfile relacionado con el usuario autenticado
        perfil_usuario, creado = UserProfile.objects.get_or_create(user=user)
        perfil_usuario.email = email
        perfil_usuario.numero_telefono = numero_telefono
        perfil_usuario.direccion = direccion
        perfil_usuario.nombre = nombre
        if imagen:
            perfil_usuario.imagen = imagen
        perfil_usuario.save()
        
        # Verificar si el usuario es propietario
        is_owner = user.is_owner

        if is_owner:
            # El usuario es propietario, redirigir a llenar los datos de VehicleOwner
            return redirect('complete_verification')
        else:
            # El usuario no es propietario, redirigir al perfil
            return redirect('perfil')
        
    return render(request, 'perfil/crear_perfil.html')

# @login_required
# def crear_perfil(request):
#     if request.method == 'POST':
#         if not UserProfile.objects.filter(user=request.user).exists():
#             form = UserProfilCreateForm(request.POST, request.FILES)
#             if form.is_valid():
#                 profile = form.save(commit=False)
#                 profile.user = request.user
#                 profile.save()
#                 # return render(request, 'perfil/crear_perfil.html')
#         else:
#             # El perfil ya existe para este usuario, puedes redirigirlo o mostrar un mensaje de error.
#             return redirect('perfil')
#     else:
#         form = UserProfilCreateForm()

#     return render(request, 'perfil/crear_perfil.html', {'form': form})


##EDITAR PERFIL
@login_required
def update_profile(request):
    # Recupera los objetos UserProfile y VehicleOwner asociados al usuario actual
    user_profile = UserProfile.objects.get(user=request.user)
    vehicle_owner_profile = VehicleOwner.objects.get(user=request.user)

     if not UserProfile.objects.filter(user=request.user).exists():
        return redirect('crear_perfil')  # Redireccionar a la vista de creación de perfil
          
    if request.method == 'POST':
        # Procesa el formulario de UserProfile
        user_profile.email = request.POST['email']
        user_profile.numero_telefono = request.POST['numero_telefono']
        user_profile.direccion = request.POST['direccion']
        user_profile.nombre = request.POST['nombre']
        if 'imagen' in request.FILES:
            user_profile.imagen = request.FILES['imagen']
        user_profile.save()

        # Procesa el formulario de VehicleOwner
        vehicle_owner_profile.id_document = request.POST['id_document']
        vehicle_owner_profile.emergency_contact = request.POST['emergency_contact']
        vehicle_owner_profile.rental_price_hourly = request.POST['rental_price_hourly']
        vehicle_owner_profile.emergency_contact = request.POST['emergency_contact']
        vehicle_owner_profile.rental_conditions = request.POST['rental_conditions']
        
        if 'foto1_dui' in request.FILES:
            vehicle_owner_profile.foto1_dui = request.FILES['foto1_dui']
        if 'foto2_dui' in request.FILES:
            vehicle_owner_profile.foto2_dui = request.FILES['foto2_dui']
        if 'foto_licencia' in request.FILES:
            vehicle_owner_profile.foto_licencia = request.FILES['foto_licencia']
        vehicle_owner_profile.save()

        return redirect('perfil')  # Redirigir a la página de perfil después de editar

    return render(request, 'perfil/editar_perfil.html', {'user_profile': user_profile, 'vehicle_owner_profile': vehicle_owner_profile})



#VISTA PARA HACER LOGIN BASADA EN FUNCION SIN ARCHIVOS FORM
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')

            # Verificar si el usuario ya tiene un perfil
            if UserProfile.objects.filter(user=user).exists():
                # El usuario ya tiene un perfil, redirigir a su perfil
                return redirect('perfil')
            else:
                # El usuario no tiene un perfil, redirigir a la creación de perfil
                return redirect('crear_perfil')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'users/login.html')

##VISTA DE LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with your desired redirect URL

## VISTA PARA VER LA CANTIDAD DE vehicle QUE ESTAN RELACIONADOS AL USUARIO
# @login_required
# def vervehiculos(request):
#     if (request.user != None and request.user.is_authenticated()):
        
@login_required
def become_owner(request):
    if request.method == "POST":
        # Obtener el usuario actual
        user = request.user

           # Verificar si el usuario ya es propietario
        if not hasattr(user, 'vehicle_owner_profile'):
            # Si no es propietario, crea un perfil de propietario y asigna los valores
            owner = VehicleOwner(
                user=user,
                id_document=request.POST.get('id_document'),
                emergency_contact=request.POST.get('emergency_contact'),
                availability_hours=request.POST.get('availability_hours'),
                rental_conditions=request.POST.get('rental_conditions')
            )

            # Maneja la carga de archivos para las fotos aquí, por ejemplo:
            owner.foto1_dui = request.FILES['foto1_dui']
            owner.foto2_dui = request.FILES['foto2_dui']
            owner.foto_licencia = request.FILES['foto_licencia']

            owner.save()
            user.vehicle_owner_profile = owner
            user.save()
            return redirect('crear_vehiculo_paso1') # Redirige a la página de inicio del propietario

        # Si el usuario no es propietario, modifica is_owner usando el modal
        if request.POST.get('is_owner') == 'true':
            user.is_owner = True
            user.save()

        return redirect('perfil')

    # Renderiza la página de become_owner
    return render(request, 'owner/become_owner.html')


# Vista para completar la información de verificación
@login_required
def complete_verification(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Procesa el formulario de información de verificación
        id_document = request.POST.get('id_document')
        emergency_contact = request.POST.get('emergency_contact')

        availability_hours = request.POST.get('availability_hours')
        rental_conditions = request.POST.get('rental_conditions')
        
        # Procesa las imágenes adjuntas si se proporcionan
        foto1_dui = request.FILES.get('foto1_dui')
        foto2_dui = request.FILES.get('foto2_dui')
        foto_licencia = request.FILES.get('foto_licencia')

        # Crea un objeto VehicleOwner relacionado con el perfil de usuario
        vehicle_owner, created = VehicleOwner.objects.get_or_create(user=user_profile.user)
        vehicle_owner.id_document = id_document
        vehicle_owner.emergency_contact = emergency_contact
        vehicle_owner.availability_hours = availability_hours
        vehicle_owner.rental_conditions = rental_conditions

        # Asigna las imágenes si se proporcionan
        if foto1_dui:
            vehicle_owner.foto1_dui = foto1_dui
        if foto2_dui:
            vehicle_owner.foto2_dui = foto2_dui
        if foto_licencia:
            vehicle_owner.foto_licencia = foto_licencia

        vehicle_owner.save()
        
        # Actualiza el atributo is_owner de la instancia de User
        request.user.is_owner = True
        request.user.save()

        return redirect('crear_vehiculo_paso1')  # Redirige al panel de control

    return render(request, 'owner/complete_verification.html')


@login_required
def ultimos_4_vehicle_list(request):
    # Filtra los vehículos del usuario autenticado y obtén los últimos 4 registros
    user_vehicles = Vehicle.objects.filter(owner=request.user).order_by('-id')[:4]

    vehicle_types = VehicleType.objects.all()
    locations = Location.objects.all()

    context = {
        'user_vehicles': user_vehicles,
        'vehicle_types': vehicle_types,
        'locations': locations
    }

    return render(request, 'after_4_vehic.html', context)

