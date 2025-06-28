from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'inscription d'un nouvel utilisateur
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    passwordConfirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'nom', 'prenom', 'phoneNumber', 'email',
            'password', 'passwordConfirm'
        ]
        extra_kwargs = {
            'nom': {'required': True},
            'prenom': {'required': True},
            'phoneNumber': {'required': True},
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        # Vérifier que les mots de passe correspondent
        if attrs['password'] != attrs['passwordConfirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        # Vérifier que le numéro de téléphone n'existe pas déjà
        phoneNumber = attrs.get('phoneNumber')
        if CustomUser.objects.filter(phoneNumber=phoneNumber).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        
        # Vérifier que l'email n'existe pas déjà
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        
        return attrs
    
    def create(self, validated_data):
        # Supprimer passwordConfirm des données validées
        validated_data.pop('passwordConfirm')
        
        # Créer l'utilisateur avec le mot de passe hashé
        user = CustomUser.objects.create_user(
            username=validated_data['phoneNumber'],  # Utiliser le numéro comme username
            **validated_data
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Sérialiseur pour la connexion utilisateur
    """
    phoneNumber = serializers.CharField(max_length=15)
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        phoneNumber = attrs.get('phoneNumber')
        password = attrs.get('password')
        
        if phoneNumber and password:
            # Nettoyer le numéro de téléphone
            phoneNumber = ''.join(filter(str.isdigit, phoneNumber))
            if not phoneNumber.startswith('228'):
                phoneNumber = '228' + phoneNumber
            phoneNumber = '+' + phoneNumber
            
            # Authentifier l'utilisateur
            user = authenticate(
                request=self.context.get('request'),
                username=phoneNumber,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    "Impossible de se connecter avec les identifiants fournis."
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    "Ce compte a été désactivé."
                )
            
            attrs['user'] = user
            attrs['phoneNumber'] = phoneNumber
        else:
            raise serializers.ValidationError(
                "Le numéro de téléphone et le mot de passe sont requis."
            )
        
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour afficher les détails d'un utilisateur
    """
    user_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'nom', 'prenom', 'phoneNumber', 'email',
            'role', 'date_creation', 'date_modification', 'is_active'
        ]
        read_only_fields = ['user_id', 'date_creation', 'date_modification']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la mise à jour d'un utilisateur
    """
    class Meta:
        model = CustomUser
        fields = ['nom', 'prenom', 'email']
    
    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Sérialiseur pour changer le mot de passe
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_passwordConfirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_passwordConfirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value 