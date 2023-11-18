# reviews/views.py
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from vehicles.models import Vehicle
from .models import Review

class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'  # Crea un archivo HTML para mostrar la lista de revisiones
    context_object_name = 'reviews'  # El nombre de la variable de contexto que se usará en la plantilla

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review_detail.html'  # Crea un archivo HTML para mostrar los detalles de la revisión
    context_object_name = 'review'  # El nombre de la variable de contexto que se usará en la plantilla
    
@login_required
def add_review(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    
    # Verifica si el usuario tiene un perfil de "renter"
    if not request.user.renter_profile:  # Supongamos que tienes un campo llamado "renter_profile" en tu modelo de usuario
        # Si el usuario no tiene un perfil de "renter", redirige a la página de creación de perfil
        return redirect('create_renter')  # Reemplaza 'crear_perfil_renter' con la URL real de creación de perfil
    
    if request.method == 'POST':
        # Procesar el formulario enviado en la plantilla
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        reviewed_by = request.user

        review = Review(vehicle=vehicle, rating=rating, comment=comment, reviewed_by=reviewed_by)
        review.save()

        return redirect('vehicle_detail', vehicle_id=vehicle.id)

    return render(request, 'review_create.html', {'vehicle': vehicle})


class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review_form.html'  # Usa el mismo archivo HTML del formulario de creación
    fields = ['rating', 'comment']  # Campos que se mostrarán en el formulario
    
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'  # Crea un archivo HTML para la confirmación de eliminación
    success_url = reverse_lazy('review-list')  # Redirige a la lista de revisiones después de eliminar