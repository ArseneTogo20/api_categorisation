from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)


# Renommage pour plus de clarté, car cette vue est maintenant pour les admins
class UserCreationByAdminView(APIView):
    """
    Vue pour la création d'un nouvel utilisateur PAR UN ADMIN.
    Seuls les administrateurs peuvent accéder à cet endpoint.
    """
    # CHangement de la permission ici
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Un admin crée le compte, mais on ne renvoie pas les tokens,
            # car ce n'est pas l'admin qui va se connecter à la place de l'utilisateur.
            # On renvoie juste les détails de l'utilisateur créé.
            return Response({
                'message': 'Utilisateur créé avec succès par un administrateur.',
                'user': UserDetailSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    Vue pour la connexion utilisateur
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Connexion réussie',
                'user': UserDetailSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Vue pour afficher et modifier le profil utilisateur
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Récupérer le profil de l'utilisateur connecté"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Modifier le profil de l'utilisateur connecté"""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil mis à jour avec succès',
                'user': UserDetailSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Vue pour changer le mot de passe
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Mettre à jour la session pour éviter la déconnexion
            update_session_auth_hash(request, user)
            
            return Response({
                'message': 'Mot de passe modifié avec succès'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    Vue pour lister tous les utilisateurs (admin seulement)
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Seuls les admins peuvent voir tous les utilisateurs
        if not self.request.user.is_admin:
            return CustomUser.objects.filter(id=self.request.user.id)
        return CustomUser.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour afficher, modifier et supprimer un utilisateur spécifique
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne peut voir que son propre profil, sauf s'il est admin
        if self.request.user.is_admin:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Un utilisateur ne peut supprimer que son propre compte, sauf s'il est admin
        if not request.user.is_admin and user.id != request.user.id:
            return Response({
                'error': 'Vous n\'avez pas la permission de supprimer ce compte'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Désactiver le compte au lieu de le supprimer
        user.is_active = False
        user.save()
        
        return Response({
            'message': 'Compte désactivé avec succès'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Vue pour la déconnexion (invalider le refresh token)
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_auth_view(request):
    """
    Vue pour vérifier si l'utilisateur est authentifié
    """
    return Response({
        'message': 'Utilisateur authentifié',
        'user': UserDetailSerializer(request.user).data
    }, status=status.HTTP_200_OK)
