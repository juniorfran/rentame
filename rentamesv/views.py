from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle, VehicleType, Location
from reviews.models import Review
from django.core.paginator import Paginator
from vehicles.models import Vehicle

def index (request):
    all_locations = Location.objects.all()
    context={
        'all_locations': all_locations
    }
    return render(request, 'base.html', context)

def your_view(request):
    is_home = request.path == 'home'
    return render(request, 'base.html', {'is_home': is_home})

def carrusel_view(request):
    image = Vehicle.objects.all()
    return render(request, 'carusel_view.html', {'image': image})

## funcion para buscar vehiculos por ubicacion
def search_results(request):
    if 'city' in request.GET:
        city_to_search = request.GET['ciudad']
        vehicles_in_city = Vehicle.objects.filter(location__ciudad=city_to_search)
        context = {'vehicles': vehicles_in_city, 'ciudad': city_to_search}
        return render(request, 'vehicle/search_results.html', context)
    else:
        # Si no se proporciona una ciudad, redirigir al formulario de búsqueda
        return redirect('search_form')
    
def search_form(request):
    all_locations = Location.objects.all()

    return render(request, 'filtro_busqueda.html', {'all_locations': all_locations})