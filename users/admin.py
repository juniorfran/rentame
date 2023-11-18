from django.contrib import admin
from .models import UserProfile, VehicleOwner, Renter, Review, User

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'numero_telefono', 'direccion', 'nombre', 'fecha_nacimeinto', 'imagen', 'create_add')
    pass
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'is_active', 'is_staff')
    pass
@admin.register(VehicleOwner)
class VehicleOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_document')
    pass
@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_document')
    pass
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'comment', 'date_added', 'reviewed_by')
    pass
