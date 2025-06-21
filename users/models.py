import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Manager pour le modèle utilisateur personnalisé.
    """
    def create_user(self, numero_de_telephone, password=None, **extra_fields):
        """
        Crée et sauvegarde un utilisateur avec le numéro de téléphone et le mot de passe.
        """
        if not numero_de_telephone:
            raise ValueError("Le numéro de téléphone est obligatoire")
        
        # Le champ 'username' est maintenant géré par le numéro de téléphone
        extra_fields.setdefault('username', numero_de_telephone)
        
        user = self.model(numero_de_telephone=numero_de_telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_de_telephone, password=None, **extra_fields):
        """
        Crée et sauvegarde un super-utilisateur.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin') # Le rôle est admin par défaut pour un superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le super-utilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le super-utilisateur doit avoir is_superuser=True.')

        return self.create_user(numero_de_telephone, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec numéro de téléphone comme identifiant principal
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Rôles disponibles
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('utilisateur', 'Utilisateur'),
    ]
    
    # Champs personnalisés
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    
    # Validateur pour le numéro de téléphone (format togolais)
    phone_regex = RegexValidator(
        regex=r'^(\+228|228)?[0-9]{8}$',
        message="Le numéro de téléphone doit être au format togolais (ex: 90123456 ou +22890123456)"
    )
    
    numero_de_telephone = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex],
        verbose_name="Numéro de téléphone"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='utilisateur',
        verbose_name="Rôle"
    )
    
    # Champs de suivi
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    is_active = models.BooleanField(default=True, verbose_name="Compte actif")
    
    # Configuration du modèle
    USERNAME_FIELD = 'numero_de_telephone'
    REQUIRED_FIELDS = ['nom', 'prenom', 'email']
    
    objects = CustomUserManager() # Assigner le nouveau manager

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        db_table = 'users'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_de_telephone})"
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"
    
    def get_short_name(self):
        return self.prenom
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def save(self, *args, **kwargs):
        # Nettoyer le numéro de téléphone
        if self.numero_de_telephone:
            # Supprimer les espaces et caractères spéciaux
            self.numero_de_telephone = ''.join(filter(str.isdigit, self.numero_de_telephone))
            # Ajouter le préfixe +228 si nécessaire
            if not self.numero_de_telephone.startswith('228'):
                self.numero_de_telephone = '228' + self.numero_de_telephone
            # Ajouter le + au début
            if not self.numero_de_telephone.startswith('+'):
                self.numero_de_telephone = '+' + self.numero_de_telephone
        
        super().save(*args, **kwargs)
