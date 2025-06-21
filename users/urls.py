from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # --- Authentication Endpoints ---
    # POST: /api/auth/login/ -> Se connecter et obtenir les tokens
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    # POST: /api/auth/logout/ -> Se déconnecter (invalider le refresh token)
    path('auth/logout/', views.logout_view, name='logout'),
    # POST: /api/auth/token/refresh/ -> Rafraîchir le token d'accès
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # GET: /api/auth/verify/ -> Vérifier si l'utilisateur est authentifié avec le token actuel
    path('auth/verify/', views.check_auth_view, name='check_auth'),

    # --- Current User Profile Endpoints ---
    # GET, PUT: /api/me/profile/ -> Obtenir ou mettre à jour le profil de l'utilisateur courant
    path('me/profile/', views.UserProfileView.as_view(), name='profile'),
    # POST: /api/me/change-password/ -> Changer le mot de passe de l'utilisateur courant
    path('me/change-password/', views.ChangePasswordView.as_view(), name='change_password'),

    # --- Admin User Management Endpoints ---
    # POST: /api/admin/create-user/ -> Créer un nouvel utilisateur (admin seulement)
    path('admin/create-user/', views.UserCreationByAdminView.as_view(), name='create_user'),
    # GET: /api/admin/get-all-users/ -> Obtenir la liste de tous les utilisateurs (admin seulement)
    path('admin/get-all-users/', views.UserListView.as_view(), name='user_list'),
    # GET, PUT, DELETE: /api/admin/user-details/<uuid:pk>/ -> Gérer un utilisateur spécifique (admin seulement)
    path('admin/user-details/<uuid:pk>/', views.UserDetailView.as_view(), name='user_detail'),
] 