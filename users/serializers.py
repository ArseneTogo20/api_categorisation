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
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'nom', 'prenom', 'numero_de_telephone', 'email',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'nom': {'required': True},
            'prenom': {'required': True},
            'numero_de_telephone': {'required': True},
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        # Vérifier que les mots de passe correspondent
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        # Vérifier que le numéro de téléphone n'existe pas déjà
        numero_de_telephone = attrs.get('numero_de_telephone')
        if CustomUser.objects.filter(numero_de_telephone=numero_de_telephone).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        
        # Vérifier que l'email n'existe pas déjà
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        
        return attrs
    
    def create(self, validated_data):
        # Supprimer password_confirm des données validées
        validated_data.pop('password_confirm')
        
        # Créer l'utilisateur avec le mot de passe hashé
        user = CustomUser.objects.create_user(
            username=validated_data['numero_de_telephone'],  # Utiliser le numéro comme username
            **validated_data
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Sérialiseur pour la connexion utilisateur
    """
    numero_de_telephone = serializers.CharField(max_length=15)
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        numero_de_telephone = attrs.get('numero_de_telephone')
        password = attrs.get('password')
        
        if numero_de_telephone and password:
            # Nettoyer le numéro de téléphone
            numero_de_telephone = ''.join(filter(str.isdigit, numero_de_telephone))
            if not numero_de_telephone.startswith('228'):
                numero_de_telephone = '228' + numero_de_telephone
            numero_de_telephone = '+' + numero_de_telephone
            
            # Authentifier l'utilisateur
            user = authenticate(
                request=self.context.get('request'),
                username=numero_de_telephone,
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
            attrs['numero_de_telephone'] = numero_de_telephone
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
            'user_id', 'nom', 'prenom', 'numero_de_telephone', 'email',
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
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value 