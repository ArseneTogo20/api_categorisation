from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour CustomUser
    """
    list_display = ('numero_de_telephone', 'nom', 'prenom', 'email', 'role', 'is_active', 'date_creation')
    list_filter = ('role', 'is_active', 'date_creation')
    search_fields = ('numero_de_telephone', 'nom', 'prenom', 'email')
    ordering = ('-date_creation',)
    
    fieldsets = (
        (None, {'fields': ('numero_de_telephone', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'email')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_creation', 'date_modification')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_de_telephone', 'nom', 'prenom', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ('id', 'date_creation', 'date_modification', 'last_login')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
